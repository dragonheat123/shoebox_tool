import Resilience.Resiliencem as res
from Floor_Layout_Syntax import Building_v2
import Floor_Layout_Syntax.Layout_graph as layout
from LCA import LCADB as lcadb

dir = '/Users/zack_sutd/NextGenHighRise Dropbox/2018(09).NGH_NextGeneration(Residential)Highrise/05_Production/_Zack/Resilience/LCA database'
LCAfilepath = dir+'/Quartz_db_2019_Jan.csv'

# LCA = lcadb.LCADB(LCAfilepath)
#
# print (LCA.LCA)
#
# print ('GWP factor for CP032 is ', LCA.factor('CP032'))

rootDir = '/Users/zack_sutd/NextGenHighRise Dropbox/2018(09).NGH_NextGeneration(Residential)Highrise/05_Production/_Zack/Resilience/new results/'

r = res.Resilience(rootDir, LCAfilepath)
decades=['2020-2040','2040-2060','2060-2080','2080-2100']
# print (r.calcFlex(total=True))
# print ('Fixed GWP ',r.accumFixedGWP(decades=decades))
# print ('Flexible GWP ',r.accumFlexGWP( strucMatID='CP042',infillMatID='CP005', decades=decades))
print (r.eval([['CP042', 'CP005'], ['CP042', 'CP006'], ['CP042', 'CP006'], ['CP042', 'CP006']], decades=decades))
# building1 = r.parcelisedBuildings[0]
# print (building1.parcelizedBuilding)
# print (building1.parcelizedBuilding[1].edges.getGWP())
# print (r.parcelisedBuildings)
# print (r.calc())