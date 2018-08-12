rm ../PNG/base*
rm ../PNG/feature*
rm ../PNG/terrain*
rm ../PNG/castle*
rm ../PNG/farm*
rm ../PNG/house*

python MapGenBase.py
python MapGenFeatures.py
python MapGenTerrain.py
python MapGenCastle.py
python MapGenFarms.py
python MapGenHouses.py
