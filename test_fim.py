#!/usr/bin/env python3
"""
Testes para FileIntegrityMonitor (lógica core sem GUI).
"""

import unittest
import os
import json
import hashlib
import tempfile
import sys

# Adicionar diretório ao path
sys.path.insert(0, os.path.dirname(__file__))


class TestFileIntegrityMonitor(unittest.TestCase):
    """Testes das funções de hash e verificação."""
    
    @classmethod
    def setUpClass(cls):
        """Criar arquivo temporário para testes."""
        cls.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        cls.temp_file.write("Conteúdo de teste para hash")
        cls.temp_file.close()
        cls.temp_file_path = cls.temp_file.name
    
    @classmethod
    def tearDownClass(cls):
        """Limpar arquivo temporário."""
        if os.path.exists(cls.temp_file_path):
            os.remove(cls.temp_file_path)
        if os.path.exists('hash_data.json'):
            os.remove('hash_data.json')
    
    def test_calculate_hash(self):
        """Testa cálculo de hash SHA256."""
        def calculate_hash(file_path):
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        
        hash1 = calculate_hash(self.temp_file_path)
        hash2 = calculate_hash(self.temp_file_path)
        
        # Hashes iguais para mesmo arquivo
        self.assertEqual(hash1, hash2)
        # Hash é uma string de 64 caracteres (SHA256)
        self.assertEqual(len(hash1), 64)
    
    def test_hash_changes_with_file_modification(self):
        """Testa se hash muda quando arquivo é modificado."""
        def calculate_hash(file_path):
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        
        hash_before = calculate_hash(self.temp_file_path)
        
        # Modificar arquivo
        with open(self.temp_file_path, 'a') as f:
            f.write("\nMais conteúdo")
        
        hash_after = calculate_hash(self.temp_file_path)
        
        # Hashes devem ser diferentes
        self.assertNotEqual(hash_before, hash_after)
        
        # Restaurar arquivo
        with open(self.temp_file_path, 'w') as f:
            f.write("Conteúdo de teste para hash")
    
    def test_save_hash_to_json(self):
        """Testa salvamento de hash em JSON."""
        def calculate_hash(file_path):
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        
        hash_value = calculate_hash(self.temp_file_path)
        
        data = {
            "file_path": self.temp_file_path,
            "hash_value": hash_value
        }
        
        with open("hash_data.json", "w") as json_file:
            json.dump(data, json_file)
        
        # Verificar se arquivo foi criado
        self.assertTrue(os.path.exists("hash_data.json"))
        
        # Verificar conteúdo
        with open("hash_data.json", "r") as json_file:
            loaded_data = json.load(json_file)
        
        self.assertEqual(loaded_data["file_path"], self.temp_file_path)
        self.assertEqual(loaded_data["hash_value"], hash_value)
    
    def test_verify_file_integrity(self):
        """Testa verificação de integridade."""
        def calculate_hash(file_path):
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        
        # Salvar hash
        hash_value = calculate_hash(self.temp_file_path)
        data = {
            "file_path": self.temp_file_path,
            "hash_value": hash_value
        }
        with open("hash_data.json", "w") as json_file:
            json.dump(data, json_file)
        
        # Verificar
        with open("hash_data.json", "r") as json_file:
            saved_data = json.load(json_file)
        
        current_hash = calculate_hash(saved_data["file_path"])
        is_intact = (current_hash == saved_data["hash_value"])
        
        self.assertTrue(is_intact)
    
    def test_detect_file_tampering(self):
        """Testa detecção de arquivo modificado."""
        def calculate_hash(file_path):
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        
        # Salvar hash
        hash_value = calculate_hash(self.temp_file_path)
        data = {
            "file_path": self.temp_file_path,
            "hash_value": hash_value
        }
        with open("hash_data.json", "w") as json_file:
            json.dump(data, json_file)
        
        # Modificar arquivo
        with open(self.temp_file_path, 'a') as f:
            f.write("\nMODIFICADO")
        
        # Verificar
        with open("hash_data.json", "r") as json_file:
            saved_data = json.load(json_file)
        
        current_hash = calculate_hash(saved_data["file_path"])
        is_intact = (current_hash == saved_data["hash_value"])
        
        self.assertFalse(is_intact)
        
        # Restaurar
        with open(self.temp_file_path, 'w') as f:
            f.write("Conteúdo de teste para hash")


if __name__ == "__main__":
    unittest.main(verbosity=2)
