{
  description = "Zen MCP Server";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs { inherit system; };
      python = pkgs.python312;
    in {
      packages.default = python.pkgs.buildPythonApplication {
        pname = "zen-mcp-server";
        version = "1.1.0";
        src = ./.;
        format = "pyproject";

        nativeBuildInputs = with python.pkgs; [ 
          setuptools 
          setuptools-scm 
          wheel 
        ];
        propagatedBuildInputs = with python.pkgs; [
          mcp google-genai openai pydantic python-dotenv
        ];

        # If packages aren't in nixpkgs, override here
        # postInstall = "ln -s $out/bin/server.py $out/bin/zen-mcp-server";
      };

      devShells.default = pkgs.mkShell {
        packages = [ 
          python 
          (python.withPackages (ps: with ps; [
            # runtime deps
            mcp google-genai openai pydantic python-dotenv
            # dev deps  
            pytest pytest-asyncio black ruff isort
          ]))
        ];
        
        # Ensure proper shared library paths
        LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
          pkgs.stdenv.cc.cc.lib
        ];
      };
    });
}