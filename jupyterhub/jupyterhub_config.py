# from oauthenticator.gitlab import GitLabOAuthenticator
from oauthenticator.github import GitHubOAuthenticator
c = get_config()  #noqa


c.JupyterHub.authenticator_class = GitHubOAuthenticator
c.GitHubOAuthenticator.allowed_users = {'yms218'}
c.GitHubOAuthenticator.admin_users = {'yms218'}

c.GitHubOAuthenticator.oauth_callback_url = 'http://localhost:8888/hub/oauth_callback'
c.GitHubOAuthenticator.client_id = 'Ov23liBv9DUmd60E7EQi'  # GitHub에서 발급받은 Client ID
c.GitHubOAuthenticator.client_secret = 'fdb66728ce8939c49024b4af299843ef2bbed42b'  # GitHub에서 발급받은 Client Secret



c.JupyterHub.port = 8888
# c.JupyterHub.ssl_key = '/etc/jupyterhub/ssl/server.key'
# c.JupyterHub.ssl_cert = '/etc/jupyterhub/ssl/server.crt'

c.Authenticator.admin_users = {'admin'}
c.PAMAuthenticator.admin_groups = {'masterG'}
                                                                                                                    


                                                                                                                    