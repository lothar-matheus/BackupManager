#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Autor: Seu Nome
Data: 05/02/2026
"""

import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from cryptography.fernet import Fernet
import base64
import hashlib


class BackupManager:
    """Gerenciador de backup de pastas"""
    
    def __init__(self):
        # Define o caminho da área de trabalho
        self.desktop_path = Path.home() / "Desktop"
        self.backup_folder = self.desktop_path / "backup"
        
    def criar_pasta_backup(self):
        """Cria a pasta de backup na área de trabalho se não existir"""
        if not self.backup_folder.exists():
            self.backup_folder.mkdir(parents=True)
            print(f"[+] Pasta de backup criada em: {self.backup_folder}")
        else:
            print(f"[+] Pasta de backup já existe em: {self.backup_folder}")
    
    def validar_caminho(self, caminho):
        """Valida se o caminho fornecido existe e é uma pasta"""
        path = Path(caminho)
        
        if not path.exists():
            print(f"[!] Erro: O caminho '{caminho}' não existe.")
            return False
        
        if not path.is_dir():
            print(f"[!] Erro: O caminho '{caminho}' não é uma pasta.")
            return False
        
        return True
    
    def criar_backup_zip(self, caminho_origem):
        """Cria um backup compactado da pasta fornecida"""
        path_origem = Path(caminho_origem)
        
        # Cria nome do arquivo ZIP com timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_pasta = path_origem.name
        nome_zip = f"{nome_pasta}_backup_{timestamp}.zip"
        caminho_zip = self.backup_folder / nome_zip
        
        print(f"\n[*] Iniciando backup de: {path_origem}")
        print(f"[*] Criando arquivo: {nome_zip}")
        
        try:
            # Cria o arquivo ZIP
            with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Percorre todos os arquivos e subpastas
                for root, dirs, files in os.walk(path_origem):
                    for file in files:
                        file_path = Path(root) / file
                        # Calcula o caminho relativo para manter a estrutura de pastas
                        arcname = file_path.relative_to(path_origem.parent)
                        zipf.write(file_path, arcname)
                        print(f"[+] Adicionado: {arcname}")
            
            # Verifica o tamanho do arquivo criado
            tamanho_mb = caminho_zip.stat().st_size / (1024 * 1024)
            
            print(f"\n[✓] Backup concluído com sucesso!")
            print(f"[✓] Arquivo salvo em: {caminho_zip}")
            print(f"[✓] Tamanho: {tamanho_mb:.2f} MB")
            
            return True
            
        except PermissionError:
            print(f"[!] Erro: Sem permissão para acessar alguns arquivos.")
            return False
        except Exception as e:
            print(f"[!] Erro ao criar backup: {str(e)}")
            return False
    
    def gerar_chave_from_senha(self, senha):
        """Gera uma chave válida do Fernet a partir de uma senha"""
        # Usa SHA-256 para criar um hash da senha
        hash_senha = hashlib.sha256(senha.encode()).digest()
        # Converte para base64 (formato esperado pelo Fernet)
        chave = base64.urlsafe_b64encode(hash_senha)
        return chave
    
    def criptografar_arquivo(self, caminho_arquivo, senha):
        """Criptografa um arquivo usando a senha fornecida"""
        try:
            # Gera a chave a partir da senha
            chave = self.gerar_chave_from_senha(senha)
            fernet = Fernet(chave)
            
            # Lê o arquivo original
            with open(caminho_arquivo, 'rb') as file:
                dados_originais = file.read()
            
            print(f"[*] Tamanho do arquivo original: {len(dados_originais)} bytes")
            
            # Criptografa os dados
            dados_criptografados = fernet.encrypt(dados_originais)
            
            print(f"[*] Tamanho após criptografia: {len(dados_criptografados)} bytes")
            
            # Salva o arquivo criptografado (adiciona .encrypted)
            caminho_criptografado = str(caminho_arquivo) + '.encrypted'
            with open(caminho_criptografado, 'wb') as file:
                file.write(dados_criptografados)
                file.flush()  # Garante que os dados sejam escritos
                os.fsync(file.fileno())  # Força a escrita no disco
            
            # Remove o arquivo original não criptografado
            os.remove(caminho_arquivo)
            
            return caminho_criptografado
            
        except Exception as e:
            print(f"[!] Erro ao criptografar: {str(e)}")
            return None
    
    def descriptografar_arquivo(self, caminho_arquivo, senha):
        """Descriptografa um arquivo usando a senha fornecida"""
        try:
            # Gera a chave a partir da senha
            chave = self.gerar_chave_from_senha(senha)
            fernet = Fernet(chave)
            
            # Lê o arquivo criptografado
            print(f"[*] Lendo arquivo criptografado...")
            with open(caminho_arquivo, 'rb') as file:
                dados_criptografados = file.read()
            
            print(f"[*] Tamanho do arquivo criptografado: {len(dados_criptografados)} bytes")
            
            # Descriptografa os dados
            print(f"[*] Descriptografando dados...")
            dados_originais = fernet.decrypt(dados_criptografados)
            
            print(f"[*] Tamanho do arquivo original: {len(dados_originais)} bytes")
            
            # Remove a extensão .encrypted do nome
            if caminho_arquivo.endswith('.encrypted'):
                caminho_descriptografado = caminho_arquivo[:-10]  # Remove '.encrypted'
            else:
                caminho_descriptografado = caminho_arquivo + '.decrypted'
            
            # Salva o arquivo descriptografado
            print(f"[*] Salvando arquivo descriptografado...")
            with open(caminho_descriptografado, 'wb') as file:
                file.write(dados_originais)
                file.flush()  # Garante que os dados sejam escritos
                os.fsync(file.fileno())  # Força a escrita no disco
            
            # Verifica se o arquivo foi criado corretamente
            if Path(caminho_descriptografado).exists():
                tamanho_salvo = Path(caminho_descriptografado).stat().st_size
                if tamanho_salvo == len(dados_originais):
                    print(f"[✓] Verificação de integridade: OK")
                else:
                    print(f"[!] Aviso: Tamanho do arquivo difere ({tamanho_salvo} vs {len(dados_originais)})")
            
            return caminho_descriptografado
            
        except Exception as e:
            print(f"[!] Erro ao descriptografar: {str(e)}")
            print("[!] Verifique se a senha está correta.")
            return None
    
    def backup_simples(self):
        """Executa o processo de backup simples"""
        print("\n" + "="*60)
        print("BACKUP SIMPLES DE PASTA")
        print("="*60)
        
        # Solicita o caminho da pasta
        caminho = input("\nDigite o caminho completo da pasta para backup: ").strip()
        
        # Remove aspas se o usuário copiou o caminho com elas
        caminho = caminho.strip('"').strip("'")
        
        # Valida o caminho
        if not self.validar_caminho(caminho):
            return False
        
        # Cria a pasta de backup se necessário
        self.criar_pasta_backup()
        
        # Executa o backup
        return self.criar_backup_zip(caminho)
    
    def backup_criptografado(self):
        """Executa o processo de backup com criptografia"""
        print("\n" + "="*60)
        print("BACKUP CRIPTOGRAFADO DE PASTA")
        print("="*60)
        
        # Solicita o caminho da pasta
        caminho = input("\nDigite o caminho completo da pasta para backup: ").strip()
        caminho = caminho.strip('"').strip("'")
        
        # Valida o caminho
        if not self.validar_caminho(caminho):
            return False
        
        # Solicita a senha para criptografia
        print("\n[*] Defina uma senha para criptografar o backup")
        print("[!] ATENÇÃO: Guarde esta senha em local seguro!")
        senha = input("Senha: ").strip()
        
        if len(senha) < 4:
            print("[!] A senha deve ter pelo menos 4 caracteres.")
            return False
        
        confirma_senha = input("Confirme a senha: ").strip()
        
        if senha != confirma_senha:
            print("[!] As senhas não coincidem!")
            return False
        
        # Cria a pasta de backup se necessário
        self.criar_pasta_backup()
        
        # Executa o backup normal primeiro
        path_origem = Path(caminho)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_pasta = path_origem.name
        nome_zip = f"{nome_pasta}_backup_{timestamp}.zip"
        caminho_zip = self.backup_folder / nome_zip
        
        print(f"\n[*] Iniciando backup criptografado de: {path_origem}")
        print(f"[*] Criando arquivo: {nome_zip}")
        
        try:
            # Cria o arquivo ZIP
            with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(path_origem):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(path_origem.parent)
                        zipf.write(file_path, arcname)
                        print(f"[+] Adicionado: {arcname}")
            
            print(f"\n[*] Criptografando o backup...")
            
            # Criptografa o arquivo ZIP
            caminho_criptografado = self.criptografar_arquivo(caminho_zip, senha)
            
            if caminho_criptografado:
                tamanho_mb = Path(caminho_criptografado).stat().st_size / (1024 * 1024)
                
                print(f"\n[✓] Backup criptografado concluído com sucesso!")
                print(f"[✓] Arquivo salvo em: {caminho_criptografado}")
                print(f"[✓] Tamanho: {tamanho_mb:.2f} MB")
                print(f"\n[!] IMPORTANTE: Guarde sua senha em local seguro!")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"[!] Erro ao criar backup: {str(e)}")
            return False
    
    def descriptografar_backup(self):
        """Descriptografa um backup criptografado"""
        print("\n" + "="*60)
        print("DESCRIPTOGRAFAR BACKUP")
        print("="*60)
        
        # Solicita o caminho do arquivo criptografado
        caminho = input("\nDigite o caminho completo do arquivo criptografado (.encrypted): ").strip()
        caminho = caminho.strip('"').strip("'")
        
        # Verifica se o arquivo existe
        if not Path(caminho).exists():
            print(f"[!] Erro: O arquivo '{caminho}' não existe.")
            return False
        
        if not Path(caminho).is_file():
            print(f"[!] Erro: O caminho '{caminho}' não é um arquivo.")
            return False
        
        # Solicita a senha
        senha = input("\nDigite a senha do backup: ").strip()
        
        print(f"\n[*] Descriptografando arquivo...")
        
        # Descriptografa o arquivo
        caminho_descriptografado = self.descriptografar_arquivo(caminho, senha)
        
        if caminho_descriptografado:
            tamanho_mb = Path(caminho_descriptografado).stat().st_size / (1024 * 1024)
            
            print(f"\n[✓] Arquivo descriptografado com sucesso!")
            print(f"[✓] Arquivo salvo em: {caminho_descriptografado}")
            print(f"[✓] Tamanho: {tamanho_mb:.2f} MB")
            
            # Verifica se é um arquivo ZIP válido
            if caminho_descriptografado.endswith('.zip'):
                try:
                    with zipfile.ZipFile(caminho_descriptografado, 'r') as zipf:
                        num_arquivos = len(zipf.namelist())
                        print(f"[✓] Arquivo ZIP válido com {num_arquivos} arquivo(s)")
                        print(f"\n[*] Você pode extrair o arquivo ZIP normalmente agora.")
                except zipfile.BadZipFile:
                    print(f"[!] ATENÇÃO: O arquivo pode estar corrompido.")
                    print(f"[!] Tente novamente ou verifique a senha.")
            else:
                print(f"\n[*] Arquivo descriptografado com sucesso.")
            
            return True
        else:
            return False


def exibir_menu():
    """Exibe o menu principal"""
    print("\n" + "="*60)
    print("BACKUP MANAGER")
    print("="*60)
    print("\n[1] Backup Simples")
    print("[2] Backup com Criptografia")
    print("[3] Descriptografar Backup")
    print("[0] Sair")
    print("="*60)


def main():
    """Função principal do programa"""
    backup_manager = BackupManager()
    
    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            backup_manager.backup_simples()
            input("\nPressione ENTER para continuar...")
        
        elif opcao == "2":
            backup_manager.backup_criptografado()
            input("\nPressione ENTER para continuar...")
        
        elif opcao == "3":
            backup_manager.descriptografar_backup()
            input("\nPressione ENTER para continuar...")
            
        elif opcao == "0":
            print("\n[*] Encerrando o programa. Até logo!")
            break
            
        else:
            print("\n[!] Opção inválida! Tente novamente.")


if __name__ == "__main__":
    main()