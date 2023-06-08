from s3contents import S3ContentsManager
import boto3
import requests
from aiobotocore.credentials import AioDeferredRefreshableCredentials
from aiobotocore.session import get_session
from s3contents.ipycompat import Bool, Unicode


class CustomS3ContentsManager(S3ContentsManager):
    iam_role = Unicode("", help="IAM role to assume").tag(
        config=True, env="JPY_S3_IAM_ROLE"
    )

    session_name = Unicode("jupyterhub", help="IAM role to assume").tag(
        config=True, env="JPY_S3_SESSION_NAME"
    )

    @property
    def sts_client(self):
        return boto3.client("sts")

    async def _refresh_credentials(self):
        token_id_response = requests.get(
            "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=aws-trust-1",
            headers={"Metadata-Flavor": "Google"},
        )
        sts_response = self.sts_client.assume_role_with_web_identity(
            DurationSeconds=3600,
            RoleArn=self.iam_role,
            RoleSessionName=self.session_name,
            WebIdentityToken=token_id_response.text,
        )
        credentials = sts_response.get("Credentials")
        return {
            "access_key": credentials.get("AccessKeyId"),
            "secret_key": credentials.get("SecretAccessKey"),
            "token": credentials.get("SessionToken"),
            "expiry_time": credentials.get("Expiration").isoformat(),
        }

    def init_s3_hook(self, instance):
        session_credentials = AioDeferredRefreshableCredentials(
            refresh_using=self._refresh_credentials,
            method="custom-assume-role-with-web-identity",
        )
        session = get_session()
        session._credentials = session_credentials
        instance.boto3_session = session
