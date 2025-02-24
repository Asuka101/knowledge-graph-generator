from pdf_processor import extract_text_from_pdf, split_into_chunks
from deepseek_integration import KnowledgeExtractor
from neo4j_connector import Neo4jConnector
from mysql_manager import MySQLManager
import os
from concurrent.futures import ThreadPoolExecutor
import signal
import logging

def build_knowledge_graph(pdf_path):
    # 初始化连接
    db = MySQLManager()
    extractor = KnowledgeExtractor()
    connector = Neo4jConnector()
    
    # 优雅退出处理
    def handle_signal(signum, frame):
        print("\n接收到终止信号，正在保存进度...")
        raise SystemExit
    
    signal.signal(signal.SIGINT, handle_signal)
    
    try:
        # 使用线程池并行处理
        with ThreadPoolExecutor(max_workers=int(os.getenv("THREAD_POOL_SIZE", 4))) as executor:
            while True:
                chunks = db.get_unprocessed_chunks(
                    batch_size=int(os.getenv("BATCH_SIZE", 5))
                )
                if not chunks:
                    break
                
                # 并行处理分块
                futures = []
                for chunk in chunks:
                    futures.append(
                        executor.submit(
                            process_chunk,
                            chunk,
                            extractor,
                            connector,
                            db
                        )
                    )
                
                # 等待本批次完成
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        logger.error(f"处理失败: {str(e)}")
                
                print(f"已完成批次: {len(chunks)}个分块")
                
    finally:
        db.close()
        connector.close()

def process_chunk(chunk, extractor, connector, db):
    """独立处理单个分块"""
    for attempt in range(int(os.getenv("MAX_RETRIES", 3))):
        try:
            data = extractor.extract_knowledge(chunk['chunk_text'])
            with connector.driver.session() as session:
                session.execute_write(
                    connector._batch_create_entities,
                    data['entities']
                )
                session.execute_write(
                    connector._batch_create_relationships,
                    data['relationships']
                )
            db.mark_processed(chunk['id'], response=data)
            return
        except Exception as e:
            if attempt == int(os.getenv("MAX_RETRIES", 3)) - 1:
                db.mark_processed(chunk['id'], success=False, error=str(e))
                logger.error(f"分块{chunk['id']}处理失败: {str(e)}")
            else:
                logger.warning(f"分块{chunk['id']}重试中({attempt+1}/{int(os.getenv('MAX_RETRIES', 3))})")

if __name__ == "__main__":
    build_knowledge_graph("教材.pdf") 