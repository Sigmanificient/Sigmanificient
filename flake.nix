{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
  };

  outputs = { nixpkgs, ... }:
    let
      forAllSystems = function:
        nixpkgs.lib.genAttrs [
          "x86_64-linux"
          "aarch64-linux"
          "x86_64-darwin"
          "aarch64-darwin"
        ]
          (system:
            let
              pkgs = nixpkgs.legacyPackages.${system};
            in
            function pkgs);
    in
    {
      devShells = forAllSystems (pkgs:
        let
          pyenv = pkgs.python310.withPackages (p: [
            p.requests
            p.black
          ]);

        in
        {
          default = pkgs.mkShell {
            packages = [
              pkgs.gnumake
              pyenv
            ];
          };
        });

      formatter = forAllSystems (pkgs: pkgs.nixpkgs-fmt);
    };
}
