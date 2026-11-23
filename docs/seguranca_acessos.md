# Política de Segurança: Gestão de Senhas e Bloqueio de Contas

## Desbloqueio de Conta no Active Directory
Contas corporativas são bloqueadas automaticamente após **5 tentativas consecutivas** de senha incorreta, permanecendo bloqueadas por 30 minutos.
- Para desbloqueio imediato antes desse prazo, o analista de suporte N1 deve validar a identidade do colaborador via chamada de vídeo interna.
- Após validar o crachá, acesse o console **Active Directory Users and Computers (ADUC)**, localize o usuário na OU `Colaboradores`, abra a aba **Account** e marque a opção **Unlock account**.

## Política de Troca de Senha
As senhas expiram obrigatoriamente a cada **90 dias**, devem conter no mínimo 12 caracteres e não podem reutilizar as últimas 6 senhas cadastradas.