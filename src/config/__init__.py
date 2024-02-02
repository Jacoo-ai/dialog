from .rasa_config import Config

# 可以在这里初始化配置，如加载配置文件等
config = {
    "rasa": Config.get_config()
}
