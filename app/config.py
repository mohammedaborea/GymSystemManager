from pydantic_settings import BaseSettings , SettingsConfigDict

class Setting(BaseSettings) : 
    DATABASE_HOSTNAME : str
    DATABASE_PORT : int 
    DATABASE_NAME:str
    DATABASE_USERNAME:str
    DATABASE_PASSWORD:str
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Setting()
