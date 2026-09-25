{
  description = "Script that prints the Gradle version in the repository";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs =
    { nixpkgs, ... }:
    let
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];
    in
    {
      packages = nixpkgs.lib.genAttrs systems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          default = pkgs.writeShellApplication {
            name = "gradlever";

            runtimeInputs = [
              pkgs.python3
            ];

            text = ''
              python ${./src/gradlever.py} "$@"
            '';
          };
        }
      );
    };
}