from simplegmail import Gmail

def enviar_email_teste():
    gmail = Gmail(client_secret_file='credentials/client_secret.json', creds_file='credentials/gmail_token.json')

    parametros = {
        "to": "henrique@ecoloop.us",
        "sender": "henriq.gcampos@gmail.com",
        "subject": "New task: Design Request",
        "msg_html": "<h1>Teste</h1><p>Customer: Teste da Silva</p><br><p>Open task https://link.com</p>",
        # O texto plano deve conter a estrutura exata do Regex
        "msg_plain": '''DESIGN REQUEST
        
        Hi Henrique, a task was assigned to you.
        
        ProjectDesignTask statusTo DoDue dateNo due date
        
        Rep Info
        Tim Matuszewski
        tim@ecoloop.us
        
        PM Info
        Ana Carolina
        ana@ecoloop.us
        
        Deal Info
        Customer: Samantha Oneil
        Address: 20 Colgate Road - Beverly, MA - 01915
        
        Open task https://app.ecoloop.us/tasks/60da1f86-341a-4cde-947d-ddf7a090acda
        
        Ecoloop Solar Solutions
        
        This is an automated message from the Ecoloop platform. Questions? support@ecoloop.us
        
        ''',
        "signature": False
    }

    mensagem = gmail.send_message(**parametros)
    print(f"Email enviado! ID: {mensagem.id}")


def enviar_email_teste2():
    gmail = Gmail(client_secret_file='credentials/client_secret.json', creds_file='credentials/gmail_token.json')

    parametros = {
        "to": "henrique@ecoloop.us",
        "sender": "henriq.gcampos@gmail.com",
        "subject": "New task: Design Request",
        "msg_html": "<h1>Teste</h1><p>Customer: Teste da Silva</p><br><p>Open task https://link.com</p>",
        # O texto plano deve conter a estrutura exata do Regex
        "msg_plain": '''DESIGN REQUEST

        Hi Henrique, a task was assigned to you.

        ProjectDesignTask statusTo DoDue dateNo due date

        Rep Info
        Tim Matuszewski
        tim@ecoloop.us

        PM Info
        Ana Carolina
        ana@ecoloop.us

        Deal Info
        Customer: Clodovil da silva
        Address: 20 Colgate Road - Beverly, MA - 01915

        Open task https://app.ecoloop.us/tasks/60da1f86-341a-4cde-947d-ddf7a090a

        Ecoloop Solar Solutions

        This is an automated message from the Ecoloop platform. Questions? support@ecoloop.us

        ''',
        "signature": False
    }

    mensagem = gmail.send_message(**parametros)
    print(f"Email enviado! ID: {mensagem.id}")


def enviar_email_teste3():
    gmail = Gmail(client_secret_file='credentials/client_secret.json', creds_file='credentials/gmail_token.json')

    parametros = {
        "to": "henrique@ecoloop.us",
        "sender": "henriq.gcampos@gmail.com",
        "subject": "New task: Design Request",
        "msg_html": "<h1>Teste</h1><p>Customer: Teste da Silva</p><br><p>Open task https://link.com</p>",
        # O texto plano deve conter a estrutura exata do Regex
        "msg_plain": '''DESIGN REQUEST

        Hi Henrique, a task was assigned to you.

        ProjectDesignTask statusTo DoDue dateNo due date

        Rep Info
        Tim Matuszewski
        tim@ecoloop.us

        PM Info
        Ana Carolina
        ana@ecoloop.us

        Deal Info
        Customer: Rogerinho do Quero
        Address: 20 Colgate Road - Beverly, MA - 01915

        Open task https://app.ecoloop.us/tasks/

        Ecoloop Solar Solutions

        This is an automated message from the Ecoloop platform. Questions? support@ecoloop.us

        ''',
        "signature": False
    }

    mensagem = gmail.send_message(**parametros)
    print(f"Email enviado! ID: {mensagem.id}")

def enviar_email_final():
    gmail = Gmail(client_secret_file='credentials/client_secret.json', creds_file='credentials/gmail_token.json')

    parametros = {
        "to": "henrique@ecoloop.us",
        "sender": "henriq.gcampos@gmail.com",
        "subject": "New task: Final Design & Production",
        "msg_html": "<h1>Teste</h1><p>Customer: Teste da Silva</p><br><p>Open task https://link.com</p>",
        # O texto plano deve conter a estrutura exata do Regex
        "msg_plain": '''FINAL DESIGN & PRODUCTION

        Hi Henrique, a task was assigned to you.
        
        Assigned toHenriqueProjectDesignTask statusTo DoDue dateNo due dateDeal ID7ab5ed87-d4bf-437b-b648-f3c49585b219
        
        Rep Info
        Darwil
        darwil@ecoloop.us
        
        PM Info
        Bruna Escarião
        bruna@ecoloop.us
        
        Deal Info
        Customer: Luis Veras
        Address: 340 Broadway - Haverhill, MA - 01832
        Financier: Enfin
        
        Open task https://app.ecoloop.us/tasks/9c4b13ee-b448-4439-a354-8137e1920431
        
        Ecoloop Solar Solutions
        
        This is an automated message from the Ecoloop platform. Questions? support@ecoloop.us
                ''',
        "signature": False
    }

    mensagem = gmail.send_message(**parametros)
    print(f"Email enviado! ID: {mensagem.id}")


def enviar_email_final2():
    gmail = Gmail(client_secret_file='credentials/client_secret.json', creds_file='credentials/gmail_token.json')

    parametros = {
        "to": "henrique@ecoloop.us",
        "sender": "henriq.gcampos@gmail.com",
        "subject": "New task: Final Design & Production",
        "msg_html": "<h1>Teste</h1><p>Customer: Teste da Silva</p><br><p>Open task https://link.com</p>",
        # O texto plano deve conter a estrutura exata do Regex
        "msg_plain": '''FINAL DESIGN & PRODUCTION

        Hi Henrique, a task was assigned to you.

        Assigned toHenriqueProjectDesignTask statusTo DoDue dateNo due dateDeal ID7ab5ed87-d4bf-437b-b648-f3c49585b219

        Rep Info
        Darwil
        darwil@ecoloop.us

        PM Info
        Bruna Escarião
        bruna@ecoloop.us

        Deal Info
        Customer: Arnaldo moura
        Address: 340 Broadway - Haverhill, MA - 01832
        Financier: Enfin

        Open task https://app.ecoloop.us/tasks/

        Ecoloop Solar Solutions

        This is an automated message from the Ecoloop platform. Questions? support@ecoloop.us
                ''',
        "signature": False
    }

    mensagem = gmail.send_message(**parametros)
    print(f"Email enviado! ID: {mensagem.id}")


def enviar_email_final3():
    gmail = Gmail(client_secret_file='credentials/client_secret.json', creds_file='credentials/gmail_token.json')

    parametros = {
        "to": "henrique@ecoloop.us",
        "sender": "henriq.gcampos@gmail.com",
        "subject": "New task: Final Design & Production",
        "msg_html": "<h1>Teste</h1><p>Customer: Teste da Silva</p><br><p>Open task https://link.com</p>",
        # O texto plano deve conter a estrutura exata do Regex
        "msg_plain": '''FINAL DESIGN & PRODUCTION

        Hi Henrique, a task was assigned to you.

        Assigned toHenriqueProjectDesignTask statusTo DoDue dateNo due dateDeal ID7ab5ed87-d4bf-437b-b648-f3c49585b219

        Rep Info
        Darwil
        darwil@ecoloop.us

        PM Info
        Bruna Escarião
        bruna@ecoloop.us

        Deal Info
        Customer: Anderson Vieira
        Address: 340 Broadway - Haverhill, MA - 01832
        Financier: Enfin

        Open task https://app.ecoloop.us/

        Ecoloop Solar Solutions

        This is an automated message from the Ecoloop platform. Questions? support@ecoloop.us
                ''',
        "signature": False
    }

    mensagem = gmail.send_message(**parametros)
    print(f"Email enviado! ID: {mensagem.id}")


# enviar_email_final()
# enviar_email_final2()
enviar_email_final3()

# enviar_email_teste()
# enviar_email_teste2()
# enviar_email_teste3()