{
  buildPythonPackage,
  flit-core,
}:
buildPythonPackage {
  pname = "malkoha";
  version = "0.0.1"
  pyproject = true;
  src = ./.;
  build-system = [ flit-core ];
  dependencies = [ ];
}
