{
  description = "Malkoha";

  inputs = {
    flake-utils = {
      url = "github:numtide/flake-utils";
    };

    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-nix = {
      url = "github:nix-community/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    {
      self,
      flake-utils,
      nixpkgs,
      pyproject-nix,
      treefmt-nix,
      ...
    }@inputs:
    flake-utils.lib.eachSystem
      [
        "aarch64-linux"
        "x86_64-linux"
      ]
      (
        system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [
              self.overlays.default
            ];
          };
          project = pyproject-nix.lib.project.loadPyproject { projectRoot = ./.; };
          python = pkgs.python3;
          treefmtEval = treefmt-nix.lib.evalModule pkgs {
            projectRootFile = "flake.nix";
            programs = {
              black.enable = true;
              nixfmt = {
                enable = true;
                package = pkgs.nixfmt-rfc-style;
              };
            };
          };
        in
        rec {
          packages.default =
            let
              attrs = project.renderers.buildPythonPackage { inherit python; };
            in
            python.pkgs.buildPythonPackage attrs;

          devShells.default =
            let
              arg = project.renderers.withPackages { inherit python; };
              pythonEnv = python.withPackages arg;
            in
            pkgs.mkShell {
              packages = [
                pkgs.gnumake
                pkgs.nodePackages.prettier
                pkgs.nixpkgs-fmt
                pkgs.cocogitto
                pkgs.python3
                pkgs.pylint
                packages.default # for testing itself
                packages.default.passthru.optional-dependencies.test
                pythonEnv
                pkgs.ruff-lsp
                pkgs.ruff
                python.pkgs.pythonPackages.pylsp-rope
                python.pkgs.pythonPackages.python-lsp-ruff
                python.pkgs.pythonPackages.python-lsp-server
              ];
            };
          formatter = treefmtEval.config.build.wrapper;
        }
      )
    // {
      overlays.default = final: prev: {
        malkoha = self.packages.${prev.system}.default;
        python3 = prev.python3.override {
          packageOverrides = final: prev: {
            malkoha = prev.pythonPackages.callPackage ./default.nix { };
          };
        };
      };
    };
}
