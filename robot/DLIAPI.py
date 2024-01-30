# 导入依赖包
import json

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkdli.v1.region.dli_region import DliRegion
from huaweicloudsdkdli.v1 import *


# 创建华为云api连接
def create_client():
    ak = "EULIXLKJQLUS62GPNIAX"
    sk = "vmoTDJVUOXVtwt8pwh5LQ6LnE2bJPDtxid7biimK"
    credentials = BasicCredentials(ak, sk)
    client = DliClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(DliRegion.value_of("cn-south-1")) \
        .build()
    return client


if __name__ == '__main__':
    client = create_client()
    jobs = client.list_sql_jobs(request=ListSqlJobsRequest())
    # 设置获取形式并转成json数据
    response = json.dumps(jobs, default=str, ensure_ascii=False)
    # 对json数据双重读取切分
    response = json.loads(response)
    print(response)