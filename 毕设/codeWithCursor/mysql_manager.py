from mysql.connector import pooling
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)

class MySQLManager:
    def __init__(self):
        self.pool = pooling.MySQLConnectionPool(
            pool_name="kg_pool",
            pool_size=int(os.getenv("MYSQL_POOL_SIZE", 5)),
            host=os.getenv("MYSQL_HOST"),
            port=os.getenv("MYSQL_PORT"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        self._init_tables()

    def get_connection(self):
        return self.pool.get_connection()

    def _init_tables(self):
        """初始化数据库表结构"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # 创建原始文本存储表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS documents (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        file_name VARCHAR(255) NOT NULL,
                        raw_text LONGTEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # 创建文本分块表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS text_chunks (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        document_id INT,
                        chunk_text TEXT NOT NULL,
                        processed BOOLEAN DEFAULT FALSE,
                        process_time TIMESTAMP NULL,
                        FOREIGN KEY (document_id) REFERENCES documents(id)
                    )
                """)
                
                # 创建处理日志表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS processing_logs (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        chunk_id INT,
                        api_response TEXT,
                        error_message TEXT,
                        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (chunk_id) REFERENCES text_chunks(id)
                    )
                """)
                conn.commit()

    def save_document(self, file_name, text):
        """保存原始文档"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO documents (file_name, raw_text) VALUES (%s, %s)",
                    (file_name, text)
                )
                conn.commit()
                return cursor.lastrowid

    def save_chunks(self, document_id, chunks):
        """保存文本分块"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                chunk_records = [(document_id, chunk) for chunk in chunks]
                cursor.executemany(
                    "INSERT INTO text_chunks (document_id, chunk_text) VALUES (%s, %s)",
                    chunk_records
                )
                conn.commit()
        
    def get_unprocessed_chunks(self, batch_size=10):
        """获取未处理的分块"""
        with self.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT * FROM text_chunks 
                    WHERE processed = FALSE 
                    ORDER BY id ASC 
                    LIMIT %s
                """, (batch_size,))
                return cursor.fetchall()
        
    def mark_processed(self, chunk_id, success=True, response=None, error=None):
        """标记分块处理状态"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE text_chunks 
                    SET processed = %s, process_time = CURRENT_TIMESTAMP 
                    WHERE id = %s
                """, (success, chunk_id))
                
                cursor.execute("""
                    INSERT INTO processing_logs 
                    (chunk_id, api_response, error_message) 
                    VALUES (%s, %s, %s)
                """, (chunk_id, str(response), error))
                
                conn.commit()

    def close(self):
        self.pool.close() 