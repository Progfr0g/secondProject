from abc import abstractmethod, ABC
from typing import Dict, List

from pydantic import BaseModel, Field, root_validator


class TagsModel(BaseModel):
    author: str
    system: str


class DataCatalogModel(BaseModel):
    database: str
    table: str


class SourceModel(BaseModel):
    type: str
    connection: str
    dataCatalog: DataCatalogModel
    incrementFields: List[str]
    incrementSortOrder: str


class SinkModel(BaseModel):
    type: str
    s3Path: str


class JobRunSettingsModel(BaseModel):
    iamRole: str


class YAMLModel(BaseModel):
    version: float
    resource: str
    name: str
    description: str
    script: str

    tags: TagsModel
    source: SourceModel
    sink: SinkModel
    jobRunSettings: JobRunSettingsModel


"""
---------------------------------------

"""

class BaseNestingSupport(BaseModel):
    @classmethod
    @abstractmethod
    def from_config_model(cls, config):
        pass

    @root_validator(pre=True)
    def traverse_sources(cls, values):
        for (name, field) in cls.__fields__.items():
            source_selector = field.field_info.extra.get("source")
            if source_selector is not None:
                source_path = source_selector.split(".")
                if len(source_path) == 0:
                    raise ValueError(
                        f"{cls.__name__}: Invalid source path: '{source_selector}'"
                    )

                pointer = values
                for selector in source_path:
                    if not selector in pointer:
                        if not field.required:
                            pointer = None
                            break

                        raise ValueError(
                            f"{cls.__name__}: Value for '{selector}' missing, path: '{source_selector}'"
                        )

                    pointer = pointer.get(selector)

                values[name] = pointer

        return values

    class Config:
        extra = "ignore"


class JSONModel(BaseNestingSupport):
    version: float
    resource: str
    name: str
    description: str
    script: str

    tags_author: str = Field(source="tags.author")
    tags_system: str = Field(source="tags.system")

    source_type: str = Field(source="source.type")
    source_connection: str = Field(source="source.connection")
    source_data_catalog_database: str = Field(source="source.dataCatalog.database")
    source_data_catalog_table: str = Field(source="source.dataCatalog.table")
    source_increment_fields: List[str] = Field(source="source.incrementFields")
    source_increment_sort_order: str = Field(source="source.incrementSortOrder")

    sink_type: str = Field(source="sink.type")
    sink_s3_path: str = Field(source="sink.s3Path")
    job_run_settings_iam_role: str = Field(source="jobRunSettings.iamRole")


class SourceModelJSON2(BaseNestingSupport):
    source_database: str = Field(source="dataCatalog.database")
    source_table_name: str = Field(source="dataCatalog.table")
    source_increment_fields: List[str] = Field(source="incrementFields")
    source_increment_sort_order: str = Field(source="incrementSortOrder")

    sink_type: str
    sink_s3_path: str

    @classmethod
    def from_config_model(cls, config: dict):
        sink_type = config["sink"]["type"]
        sink_s3_path = config["sink"]["s3Path"]



class JSONModel2(BaseNestingSupport):
    resource: str
    job_name: str = Field(source="name")
    job_description: str = Field(source="description")
    script: str

    iam_role_arn: str = Field(source="jobRunSettings.iamRole")
    connection: str = Field(source="source.connection")

    tags_author: TagsModel = Field(source="tags")

    max_concurrent_runs: int = 1

    job_default_arguments: SourceModelJSON2

    @classmethod
    def from_config_model(cls, config: dict):
        job_default_arguments = SourceModelJSON2.from_config_model(config)

