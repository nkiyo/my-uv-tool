import boto3
from langchain_aws import ChatBedrock
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

from pydantic import BaseModel, Field
from typing import List

class DocumentSchema(BaseModel):
    title: str = Field(description="ドキュメントのタイトル")
    summary: str = Field(description="全体の要約")
    # sections: List[str] = Field(description="各セクションの要点")


def run_cli() -> None:
    print("### hoge ###") 

    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="ap-northeast-1",  # 利用リージョン
    )

    llm = ChatBedrock(
        client=bedrock_runtime,
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs={
            "temperature": 0,
            "max_tokens": 1024,
        },
    )

    parser = PydanticOutputParser(pydantic_object=DocumentSchema)

    prompt = PromptTemplate(
    template="""
    以下の Markdown を読み、指定された JSON スキーマに変換してください。
    
    {format_instructions}
    
    Markdown:
    {markdown}
    """,
        input_variables=["markdown"],
        partial_variables={
            "format_instructions": parser.get_format_instructions()
        },
    )

    chain = prompt | llm | parser
    markdown_text = "#ほげほげ  こんにちは"
    result = chain.invoke({"markdown": markdown_text})
