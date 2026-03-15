CREATE SCHEMA IF NOT EXISTS db_loja;

SET search_path TO db_loja;

-- -----------------------------------------------------
-- Table Cliente
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Cliente (
  idCliente SERIAL NOT NULL,
  nome VARCHAR(45) NOT NULL,
  email VARCHAR(45) NOT NULL,
  cpf VARCHAR(45) NOT NULL,
  senha VARCHAR(45) NOT NULL,
  PRIMARY KEY (idCliente)
);

CREATE UNIQUE INDEX email_Cliente_UNIQUE ON Cliente (email ASC);

-- -----------------------------------------------------
-- Table Lojas
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Lojas (
  idLojas SERIAL NOT NULL,
  Nome VARCHAR(45) NOT NULL,
  email VARCHAR(45) NOT NULL,
  qtsVendas INTEGER NOT NULL,
  ganhoVendas DECIMAL(10,3) NOT NULL,
  cnpj VARCHAR(45) NOT NULL,
  PRIMARY KEY (idLojas)
);

CREATE UNIQUE INDEX email_Lojas_UNIQUE ON Lojas (email ASC);
CREATE UNIQUE INDEX cnpj_Lojas_UNIQUE ON Lojas (cnpj ASC);

-- -----------------------------------------------------
-- Table Endereco
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Endereco (
  idEndereco SERIAL NOT NULL,
  Rua VARCHAR(15) NOT NULL,
  Numero VARCHAR(15) NULL,
  Bairro VARCHAR(45) NULL,
  Cidade_Estado VARCHAR(45) NULL,
  idCliente INTEGER NOT NULL,
  PRIMARY KEY (idEndereco),
  CONSTRAINT fk_Endereco_Cliente1
    FOREIGN KEY (idCliente)
    REFERENCES Cliente (idCliente)
    ON DELETE CASCADE -- Se o cliente for deletado, apaga o endereço
    ON UPDATE CASCADE
);

CREATE INDEX fk_Endereco_Cliente1_idx ON Endereco (idCliente ASC);

-- -----------------------------------------------------
-- Table Produto
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Produto (
  idProduto SERIAL NOT NULL,
  nome VARCHAR(100) NOT NULL,
  preco DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (idProduto)
);

-- -----------------------------------------------------
-- Table Item_Venda
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Item_Venda (
  idItem SERIAL NOT NULL,
  Produto_idProduto INTEGER NOT NULL,
  idLojas INTEGER NOT NULL,
  PRIMARY KEY (idItem),
  CONSTRAINT fk_Item_Venda_Produto1
    FOREIGN KEY (Produto_idProduto)
    REFERENCES Produto (idProduto)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_Item_Venda_Lojas1
    FOREIGN KEY (idLojas)
    REFERENCES Lojas (idLojas)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE INDEX fk_Item_Venda_Produto1_idx ON Item_Venda (Produto_idProduto ASC);
CREATE INDEX fk_Item_Venda_Lojas1_idx ON Item_Venda (idLojas ASC);

-- -----------------------------------------------------
-- Table Carrinho
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Carrinho (
  idCarrinho SERIAL NOT NULL,
  Item_idItem INTEGER NOT NULL,
  PRIMARY KEY (idCarrinho),
  CONSTRAINT fk_Carrinho_Item1
    FOREIGN KEY (Item_idItem)
    REFERENCES Item_Venda (idItem)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE INDEX fk_Carrinho_Item1_idx ON Carrinho (Item_idItem ASC);

-- -----------------------------------------------------
-- Table Venda
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Venda (
  idVenda SERIAL NOT NULL,
  dataVenda DATE NOT NULL DEFAULT CURRENT_DATE,
  Valor_total DECIMAL(10,2) NOT NULL,
  Pagamento_idTransacao INTEGER NOT NULL,
  idLojas INTEGER NOT NULL,
  idEndereco INTEGER NOT NULL,
  Cliente_idCliente INTEGER NOT NULL,
  Carrinho_idCarrinho INTEGER NOT NULL,
  PRIMARY KEY (idVenda),
  CONSTRAINT fk_Venda_Lojas1
    FOREIGN KEY (idLojas)
    REFERENCES Lojas (idLojas)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_Venda_Endereco1
    FOREIGN KEY (idEndereco)
    REFERENCES Endereco (idEndereco)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_Venda_Cliente1
    FOREIGN KEY (Cliente_idCliente)
    REFERENCES Cliente (idCliente)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_Venda_Carrinho1
    FOREIGN KEY (Carrinho_idCarrinho)
    REFERENCES Carrinho (idCarrinho)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE INDEX fk_Venda_Lojas1_idx ON Venda (idLojas ASC);
CREATE INDEX fk_Venda_Endereco1_idx ON Venda (idEndereco ASC);
CREATE INDEX fk_Venda_Cliente1_idx ON Venda (Cliente_idCliente ASC);
CREATE INDEX fk_Venda_Carrinho1_idx ON Venda (Carrinho_idCarrinho ASC);

-- -----------------------------------------------------
-- Table Pix
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Pix (
  idPix SERIAL NOT NULL,
  chave VARCHAR(45) NOT NULL,
  dataTransacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(45) NOT NULL,
  PRIMARY KEY (idPix)
);

CREATE UNIQUE INDEX chave_UNIQUE ON Pix (chave ASC);

-- -----------------------------------------------------
-- Table CartaoCredito
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS CartaoCredito (
  NumeroCartao SERIAL NOT NULL,
  Numero VARCHAR(45) NOT NULL,
  nome VARCHAR(45) NOT NULL,
  data_expiracao DATE NOT NULL,
  codigo_seguranca INTEGER NOT NULL,
  PRIMARY KEY (NumeroCartao)
);

CREATE UNIQUE INDEX Numero_CC_UNIQUE ON CartaoCredito (Numero ASC);
CREATE UNIQUE INDEX codigo_seguranca_CC_UNIQUE ON CartaoCredito (codigo_seguranca ASC);

-- -----------------------------------------------------
-- Table CartaoDebito
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS CartaoDebito (
  idCartaoDebito SERIAL NOT NULL,
  Numero VARCHAR(45) NOT NULL,
  nome VARCHAR(45) NOT NULL,
  data_expiracao DATE NOT NULL,
  codigo_seguranca INTEGER NOT NULL,
  PRIMARY KEY (idCartaoDebito)
);

CREATE UNIQUE INDEX Numero_CD_UNIQUE ON CartaoDebito (Numero ASC);

-- -----------------------------------------------------
-- Table Pagamento
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Pagamento (
  banco VARCHAR(45) NOT NULL,
  comprovante VARCHAR(45) NULL,
  Pix_idPix INTEGER NULL,
  CartaoCredito_NumeroCartao INTEGER NULL,
  CartaoDebito_idCartaoDebito INTEGER NULL,
  idTransacao SERIAL NOT NULL,
  PRIMARY KEY (idTransacao),
  CONSTRAINT fk_Pagamento_Pix1
    FOREIGN KEY (Pix_idPix)
    REFERENCES Pix (idPix)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_Pagamento_CartaoCredito1
    FOREIGN KEY (CartaoCredito_NumeroCartao)
    REFERENCES CartaoCredito (NumeroCartao)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_Pagamento_CartaoDebito1
    FOREIGN KEY (CartaoDebito_idCartaoDebito)
    REFERENCES CartaoDebito (idCartaoDebito)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE INDEX fk_Pagamento_Pix1_idx ON Pagamento (Pix_idPix ASC);
CREATE INDEX fk_Pagamento_CartaoCredito1_idx ON Pagamento (CartaoCredito_NumeroCartao ASC);
CREATE INDEX fk_Pagamento_CartaoDebito1_idx ON Pagamento (CartaoDebito_idCartaoDebito ASC);

-- -----------------------------------------------------
-- Table Estoque
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS Estoque (
  Produto_idProduto INTEGER NOT NULL,
  disponivel VARCHAR(45) NOT NULL DEFAULT '0',
  PRIMARY KEY (Produto_idProduto),
  CONSTRAINT fk_Estoque_Produto1
    FOREIGN KEY (Produto_idProduto)
    REFERENCES Produto (idProduto)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);