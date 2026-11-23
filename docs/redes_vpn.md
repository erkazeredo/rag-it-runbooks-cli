# Runbook: Conexão VPN Corporativa e Falhas de DNS

## Configuração Inicial
Para acessar a rede interna remotamente, utilize o cliente OpenVPN versão 2.6 ou superior com o perfil `corp-sp-gateway.ovpn`. A autenticação exige usuário do Active Directory e token MFA gerado no aplicativo Authenticator.

## Erro Comum: Conectado mas sem acesso a sistemas internos (Erro 619)
Se a VPN conectar com sucesso mas os sistemas internos (`intranet.empresa.local`) não carregarem:
1. Abra o terminal como administrador.
2. Execute o comando `ipconfig /flushdns` para limpar o cache local.
3. Verifique se o adaptador TAP-Windows está configurado para obter DNS automaticamente (`10.20.0.2`).
4. Caso o problema persista após 2 tentativas, abra um chamado na fila **Infra-Redes** informando o seu IP público atual.