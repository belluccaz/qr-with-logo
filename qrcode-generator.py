import qrcode
from PIL import Image

def qrcode_generator(url, logo_path, qr_output_path, logo_size=0.4):
    """
    Gera um QR code para a URL especificada e insere um logotipo no centro.

    Parâmetros:
    - url: O URL ou texto para o qual o QR code será gerado.
    - logo_path: Caminho para a imagem do logotipo.
    - qr_output_path: Caminho onde o QR code gerado será salvo.
    - logo_size: Tamanho do logotipo como uma fração do QR code (padrão é 0.4).
    """
    # Gerar o QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Alta correção de erro para permitir inserção de logotipo
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Criar a imagem do QR code
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGBA')
    
    # Abrir o logotipo
    logo = Image.open(logo_path)
    
    # Verificar se o logotipo está no modo RGBA (com suporte a transparência)
    if logo.mode != 'RGBA':
        logo = logo.convert('RGBA')
    
    # Calcular o tamanho do logotipo em relação ao tamanho do QR code
    qr_width, qr_height = qr_img.size
    logo_width = int(qr_width * logo_size)
    logo_height = int(qr_height * logo_size)
    logo = logo.resize((logo_width, logo_height), Image.LANCZOS)
    
    # Criar um espaço em branco no centro do QR code
    logo_position = ((qr_width - logo_width) // 2, (qr_height - logo_height) // 2)
    qr_white_area = Image.new('RGBA', (logo_width, logo_height), (255, 255, 255, 0))
    
    # Colocar o espaço em branco no centro do QR code
    qr_img.paste(qr_white_area, logo_position)

    # Colocar o logotipo no QR code
    qr_img.paste(logo, logo_position, mask=logo)
    
    # Salvar a imagem final com uma extensão de arquivo adequada
    qr_img.save(f"{qr_output_path}.png")
    print(f"QR code com logotipo salvo em {qr_output_path}.png")

# Exemplo de uso da função
qrcode_generator(
    url="https://pedrocpaes.github.io/portfolio/",
    logo_path="./assets/logotipo-peu2.png",
    qr_output_path="qrcode-peu"
)
