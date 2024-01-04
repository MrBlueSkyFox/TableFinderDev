from pydantic import (
    Field, ConfigDict,
)

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(extra='allow')
    tesseract_path: str = Field(
        default=r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        description="Path to tesseract exe for OCR"
    )
    transformer_cache: str = Field(
        default=r"models/",
        description="Path to transformer  models"
    )
    easy_ocr_cache: str = Field(
        default=r"models/easy_ocr",
        description="Path to Easy ocr models for OCR"
    )

    table_detection_model_name: str = Field(
        default="microsoft/table-transformer-detection"
    )
    table_layout_model_name: str = Field(
        default="microsoft/table-transformer-structure-recognition"
    )
    table_detection_minimum_threshold: float = Field(
        default=0.8
    )


class SettingsCLI(Settings):
    path_to_image: str
    output_dir: str
    use_deskew: bool = Field(
        default=False,
        description="Apply deskew for every image by default"
    )


class SettingsWeb(Settings):
    ...
