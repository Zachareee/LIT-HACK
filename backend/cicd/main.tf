terraform {
#   cloud {
#     organization = "LIT-HACK"
#     workspaces {
#       name = "backend"
#     }
#   }

  required_providers {
    ic = {
        source = "dfinity/ic"
    }
  }
}

provider "ic" {
  endpoint = "http://localhost:4943"
}

resource "ic_canister" "backend" {
}

output "canister_id" {
  value = ic_canister.backend.id
}