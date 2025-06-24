provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "windsor-rg"
  location = "East US"
}

resource "azurerm_virtual_network" "vnet" {
  name                = "windsor-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_postgresql_flexible_server" "db" {
  name                   = "windsordb"
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  version                = "13"
  administrator_login    = "pgadmin"
  administrator_password = "P@ssword123!"
  storage_mb             = 32768
  sku_name               = "B1ms"
}
