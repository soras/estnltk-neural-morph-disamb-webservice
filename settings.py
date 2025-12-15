from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    max_content_length: int = 200000
    model_path: str = "softmax_emb_cat_sum/"

settings = Settings()