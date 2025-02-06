{
  buildPythonPackage,
  flit-core,
}:
buildPythonPackage {
  pname = "malkoha";
  pyproject = true;
  src = ./.;
  build-system = [ flit-core ];
  dependencies = [ ];
}
