
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ADD CADENA CAT CONT COPY DELETE DESTINO DIR EDIT EXECUTE FDISK FILE1 FILE2 FIT FS FS_VAL GRP GUION ID IGUAL LETRAS_FIT LETRA_MKDISK LOGIN LOGOUT MKDIR MKDISK MKFILE MKFS MKGRP MKUSR MOUNT NAME NUM PASS PATH PAUSE R REMOVE RENAME REP RMDISK RMGRP RMUSR RUTA SIZE STRING TYPE UNIT UNMOUNT USERcomando : MKDISK atributosmatributosm : atributosm atributom\n                 | atributomatributom : GUION PATH DIR\n                 | GUION FIT STRING\n                 | GUION UNIT STRING\n                 | GUION SIZE STRINGcomando : FDISK atributosatributos : atributos atributo\n                 | atributoatributo : GUION PATH DIR\n                | GUION TYPE STRING\n                | GUION UNIT STRING\n                | GUION NAME STRING\n                | GUION SIZE STRING\n                | GUION FIT STRING\n                | GUION ADD STRING\n                | GUION DELETEcomando : RMDISK GUION PATH DIRcomando : MOUNT atributos_mountatributos_mount : atributos_mount atributo_mm\n                 | atributo_mmatributo_mm : GUION PATH DIR\n                   | GUION NAME STRINGcomando : UNMOUNT GUION ID STRINGcomando : MKFS atributos_mkfsatributos_mkfs : atributos_mkfs atributosSolo_mkfs\n                        | atributosSolo_mkfsatributosSolo_mkfs : GUION ID STRING\n                            | GUION TYPE STRINGcomando : LOGIN atributos_loginatributos_login : atributos_login atributosSolo_login\n                        | atributosSolo_loginatributosSolo_login :  GUION USER STRING\n                            | GUION PASS STRING\n                            | GUION ID STRINGcomando : LOGOUTcomando : MKGRP GUION NAME STRINGcomando : RMGRP GUION NAME STRINGcomando : MKUSR atributos_mkusratributos_mkusr : atributos_mkusr atributosSolo_mkusr\n                        | atributosSolo_mkusratributosSolo_mkusr :  GUION USER STRING\n                            | GUION PASS STRING\n                            | GUION GRP STRINGcomando : RMUSR GUION USER STRINGcomando : MKFILE atributos_mkfileatributos_mkfile : atributos_mkfile atributosSolo_mkfile\n                        | atributosSolo_mkfileatributosSolo_mkfile : GUION PATH DIR\n                            | GUION SIZE STRING\n                            | GUION CONT STRING\n                            | GUION Rcomando : CAT listaFilesCATlistaFilesCAT : listaFilesCAT atributosSolo_CAT\n                        | atributosSolo_CATatributosSolo_CAT : GUION FILE2 STRING\n                         | GUION FILE1 STRINGcomando : REMOVE GUION PATH DIRcomando : EDIT listas_editlistas_edit : listas_edit atributosSolo_EDIT\n                        | atributosSolo_EDITatributosSolo_EDIT : GUION PATH DIR\n                         |  GUION CONT DIRcomando : RENAME lista_renamelista_rename : lista_rename atributosSolo_RENAME\n                        | atributosSolo_RENAMEatributosSolo_RENAME : GUION PATH DIR\n                            | GUION NAME STRINGcomando : MKDIR lista_mkdirlista_mkdir : lista_mkdir atributosSolo_MKDIR\n                        | atributosSolo_MKDIRatributosSolo_MKDIR : GUION PATH DIR\n                           | GUION Rcomando : COPY lista_copylista_copy : lista_copy atributosSolo_COPY\n                        | atributosSolo_COPYatributosSolo_COPY : GUION PATH DIR\n                          | GUION DESTINO DIRcomando : EXECUTE GUION PATH DIRcomando : REP lista_replista_rep : lista_rep atributosSolo_REP\n                        | atributosSolo_REPatributosSolo_REP : GUION ID STRING\n                         | GUION PATH DIR\n                         | GUION NAME STRING\n                         | GUION RUTA DIRcomando : PAUSE '
    
_lr_action_items = {'MKDISK':([0,],[2,]),'FDISK':([0,],[3,]),'RMDISK':([0,],[4,]),'MOUNT':([0,],[5,]),'UNMOUNT':([0,],[6,]),'MKFS':([0,],[7,]),'LOGIN':([0,],[8,]),'LOGOUT':([0,],[9,]),'MKGRP':([0,],[10,]),'RMGRP':([0,],[11,]),'MKUSR':([0,],[12,]),'RMUSR':([0,],[13,]),'MKFILE':([0,],[14,]),'CAT':([0,],[15,]),'REMOVE':([0,],[16,]),'EDIT':([0,],[17,]),'RENAME':([0,],[18,]),'MKDIR':([0,],[19,]),'COPY':([0,],[20,]),'EXECUTE':([0,],[21,]),'REP':([0,],[22,]),'PAUSE':([0,],[23,]),'$end':([1,9,23,24,25,27,28,31,32,35,36,38,39,43,44,47,48,50,51,54,55,57,58,60,61,63,64,67,68,70,75,83,85,89,92,98,103,107,108,112,115,118,120,121,125,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,],[0,-37,-88,-1,-3,-8,-10,-20,-22,-26,-28,-31,-33,-40,-42,-47,-49,-54,-56,-60,-62,-65,-67,-70,-72,-75,-77,-81,-83,-2,-9,-18,-21,-27,-32,-41,-48,-53,-55,-61,-66,-71,-74,-76,-82,-4,-5,-6,-7,-11,-12,-13,-14,-15,-16,-17,-19,-23,-24,-25,-29,-30,-34,-35,-36,-38,-39,-43,-44,-45,-46,-50,-51,-52,-57,-58,-59,-63,-64,-68,-69,-73,-78,-79,-80,-84,-85,-86,-87,]),'GUION':([2,3,4,5,6,7,8,10,11,12,13,14,15,16,17,18,19,20,21,22,24,25,27,28,31,32,35,36,38,39,43,44,47,48,50,51,54,55,57,58,60,61,63,64,67,68,70,75,83,85,89,92,98,103,107,108,112,115,118,120,121,125,130,131,132,133,134,135,136,137,138,139,140,142,143,145,146,147,148,149,152,153,154,156,157,158,159,160,162,163,164,165,166,167,168,170,171,172,173,],[26,29,30,33,34,37,40,41,42,45,46,49,52,53,56,59,62,65,66,69,26,-3,29,-10,33,-22,37,-28,40,-33,45,-42,49,-49,52,-56,56,-62,59,-67,62,-72,65,-77,69,-83,-2,-9,-18,-21,-27,-32,-41,-48,-53,-55,-61,-66,-71,-74,-76,-82,-4,-5,-6,-7,-11,-12,-13,-14,-15,-16,-17,-23,-24,-29,-30,-34,-35,-36,-43,-44,-45,-50,-51,-52,-57,-58,-63,-64,-68,-69,-73,-78,-79,-84,-85,-86,-87,]),'PATH':([26,29,30,33,49,53,56,59,62,65,66,69,],[71,76,84,86,104,111,113,116,119,122,124,127,]),'FIT':([26,29,],[72,81,]),'UNIT':([26,29,],[73,78,]),'SIZE':([26,29,49,],[74,80,105,]),'TYPE':([29,37,],[77,91,]),'NAME':([29,33,41,42,59,69,],[79,87,96,97,117,128,]),'ADD':([29,],[82,]),'DELETE':([29,],[83,]),'ID':([34,37,40,69,],[88,90,95,126,]),'USER':([40,45,46,],[93,99,102,]),'PASS':([40,45,],[94,100,]),'GRP':([45,],[101,]),'CONT':([49,56,],[106,114,]),'R':([49,62,],[107,120,]),'FILE2':([52,],[109,]),'FILE1':([52,],[110,]),'DESTINO':([65,],[123,]),'RUTA':([69,],[129,]),'DIR':([71,76,84,86,104,111,113,114,116,119,122,123,124,127,129,],[130,134,141,142,156,161,162,163,164,166,167,168,169,171,173,]),'STRING':([72,73,74,77,78,79,80,81,82,87,88,90,91,93,94,95,96,97,99,100,101,102,105,106,109,110,117,126,128,],[131,132,133,135,136,137,138,139,140,143,144,145,146,147,148,149,150,151,152,153,154,155,157,158,159,160,165,170,172,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'comando':([0,],[1,]),'atributosm':([2,],[24,]),'atributom':([2,24,],[25,70,]),'atributos':([3,],[27,]),'atributo':([3,27,],[28,75,]),'atributos_mount':([5,],[31,]),'atributo_mm':([5,31,],[32,85,]),'atributos_mkfs':([7,],[35,]),'atributosSolo_mkfs':([7,35,],[36,89,]),'atributos_login':([8,],[38,]),'atributosSolo_login':([8,38,],[39,92,]),'atributos_mkusr':([12,],[43,]),'atributosSolo_mkusr':([12,43,],[44,98,]),'atributos_mkfile':([14,],[47,]),'atributosSolo_mkfile':([14,47,],[48,103,]),'listaFilesCAT':([15,],[50,]),'atributosSolo_CAT':([15,50,],[51,108,]),'listas_edit':([17,],[54,]),'atributosSolo_EDIT':([17,54,],[55,112,]),'lista_rename':([18,],[57,]),'atributosSolo_RENAME':([18,57,],[58,115,]),'lista_mkdir':([19,],[60,]),'atributosSolo_MKDIR':([19,60,],[61,118,]),'lista_copy':([20,],[63,]),'atributosSolo_COPY':([20,63,],[64,121,]),'lista_rep':([22,],[67,]),'atributosSolo_REP':([22,67,],[68,125,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> comando","S'",1,None,None,None),
  ('comando -> MKDISK atributosm','comando',2,'p_comando_mkdisk','main.py',278),
  ('atributosm -> atributosm atributom','atributosm',2,'p_atributosM','main.py',339),
  ('atributosm -> atributom','atributosm',1,'p_atributosM','main.py',340),
  ('atributom -> GUION PATH DIR','atributom',3,'p_atributoM','main.py',348),
  ('atributom -> GUION FIT STRING','atributom',3,'p_atributoM','main.py',349),
  ('atributom -> GUION UNIT STRING','atributom',3,'p_atributoM','main.py',350),
  ('atributom -> GUION SIZE STRING','atributom',3,'p_atributoM','main.py',351),
  ('comando -> FDISK atributos','comando',2,'p_comando_fdisk','main.py',358),
  ('atributos -> atributos atributo','atributos',2,'p_atributos','main.py',452),
  ('atributos -> atributo','atributos',1,'p_atributos','main.py',453),
  ('atributo -> GUION PATH DIR','atributo',3,'p_atributo','main.py',461),
  ('atributo -> GUION TYPE STRING','atributo',3,'p_atributo','main.py',462),
  ('atributo -> GUION UNIT STRING','atributo',3,'p_atributo','main.py',463),
  ('atributo -> GUION NAME STRING','atributo',3,'p_atributo','main.py',464),
  ('atributo -> GUION SIZE STRING','atributo',3,'p_atributo','main.py',465),
  ('atributo -> GUION FIT STRING','atributo',3,'p_atributo','main.py',466),
  ('atributo -> GUION ADD STRING','atributo',3,'p_atributo','main.py',467),
  ('atributo -> GUION DELETE','atributo',2,'p_atributo','main.py',468),
  ('comando -> RMDISK GUION PATH DIR','comando',4,'p_comando_rmdisk','main.py',479),
  ('comando -> MOUNT atributos_mount','comando',2,'p_comando_mount','main.py',497),
  ('atributos_mount -> atributos_mount atributo_mm','atributos_mount',2,'p_atributos_mount','main.py',536),
  ('atributos_mount -> atributo_mm','atributos_mount',1,'p_atributos_mount','main.py',537),
  ('atributo_mm -> GUION PATH DIR','atributo_mm',3,'p_atributo_mount','main.py',545),
  ('atributo_mm -> GUION NAME STRING','atributo_mm',3,'p_atributo_mount','main.py',546),
  ('comando -> UNMOUNT GUION ID STRING','comando',4,'p_comando_unmount','main.py',552),
  ('comando -> MKFS atributos_mkfs','comando',2,'p_comando_mkfs','main.py',569),
  ('atributos_mkfs -> atributos_mkfs atributosSolo_mkfs','atributos_mkfs',2,'p_atributos_mkfs','main.py',612),
  ('atributos_mkfs -> atributosSolo_mkfs','atributos_mkfs',1,'p_atributos_mkfs','main.py',613),
  ('atributosSolo_mkfs -> GUION ID STRING','atributosSolo_mkfs',3,'p_atributoSolo_mkfs','main.py',621),
  ('atributosSolo_mkfs -> GUION TYPE STRING','atributosSolo_mkfs',3,'p_atributoSolo_mkfs','main.py',622),
  ('comando -> LOGIN atributos_login','comando',2,'p_comando_login','main.py',628),
  ('atributos_login -> atributos_login atributosSolo_login','atributos_login',2,'p_atributos_login','main.py',667),
  ('atributos_login -> atributosSolo_login','atributos_login',1,'p_atributos_login','main.py',668),
  ('atributosSolo_login -> GUION USER STRING','atributosSolo_login',3,'p_atributoSolo_login','main.py',676),
  ('atributosSolo_login -> GUION PASS STRING','atributosSolo_login',3,'p_atributoSolo_login','main.py',677),
  ('atributosSolo_login -> GUION ID STRING','atributosSolo_login',3,'p_atributoSolo_login','main.py',678),
  ('comando -> LOGOUT','comando',1,'p_comando_logout','main.py',684),
  ('comando -> MKGRP GUION NAME STRING','comando',4,'p_comando_mkgrp','main.py',697),
  ('comando -> RMGRP GUION NAME STRING','comando',4,'p_comando_rmgrp','main.py',714),
  ('comando -> MKUSR atributos_mkusr','comando',2,'p_comando_mkusr','main.py',731),
  ('atributos_mkusr -> atributos_mkusr atributosSolo_mkusr','atributos_mkusr',2,'p_atributos_mkusr','main.py',761),
  ('atributos_mkusr -> atributosSolo_mkusr','atributos_mkusr',1,'p_atributos_mkusr','main.py',762),
  ('atributosSolo_mkusr -> GUION USER STRING','atributosSolo_mkusr',3,'p_atributoSolo_mkusr','main.py',770),
  ('atributosSolo_mkusr -> GUION PASS STRING','atributosSolo_mkusr',3,'p_atributoSolo_mkusr','main.py',771),
  ('atributosSolo_mkusr -> GUION GRP STRING','atributosSolo_mkusr',3,'p_atributoSolo_mkusr','main.py',772),
  ('comando -> RMUSR GUION USER STRING','comando',4,'p_comando_rmusr','main.py',779),
  ('comando -> MKFILE atributos_mkfile','comando',2,'p_comando_mkfile','main.py',803),
  ('atributos_mkfile -> atributos_mkfile atributosSolo_mkfile','atributos_mkfile',2,'p_atributos_mkfile','main.py',885),
  ('atributos_mkfile -> atributosSolo_mkfile','atributos_mkfile',1,'p_atributos_mkfile','main.py',886),
  ('atributosSolo_mkfile -> GUION PATH DIR','atributosSolo_mkfile',3,'p_atributoSolo_mkfile','main.py',894),
  ('atributosSolo_mkfile -> GUION SIZE STRING','atributosSolo_mkfile',3,'p_atributoSolo_mkfile','main.py',895),
  ('atributosSolo_mkfile -> GUION CONT STRING','atributosSolo_mkfile',3,'p_atributoSolo_mkfile','main.py',896),
  ('atributosSolo_mkfile -> GUION R','atributosSolo_mkfile',2,'p_atributoSolo_mkfile','main.py',897),
  ('comando -> CAT listaFilesCAT','comando',2,'p_comando_cat','main.py',914),
  ('listaFilesCAT -> listaFilesCAT atributosSolo_CAT','listaFilesCAT',2,'p_listaFilesCAT','main.py',988),
  ('listaFilesCAT -> atributosSolo_CAT','listaFilesCAT',1,'p_listaFilesCAT','main.py',989),
  ('atributosSolo_CAT -> GUION FILE2 STRING','atributosSolo_CAT',3,'p_atributoSolo_CAT','main.py',998),
  ('atributosSolo_CAT -> GUION FILE1 STRING','atributosSolo_CAT',3,'p_atributoSolo_CAT','main.py',999),
  ('comando -> REMOVE GUION PATH DIR','comando',4,'p_comando_remove','main.py',1008),
  ('comando -> EDIT listas_edit','comando',2,'p_comando_edit','main.py',1020),
  ('listas_edit -> listas_edit atributosSolo_EDIT','listas_edit',2,'p_listaFilesEDIT','main.py',1046),
  ('listas_edit -> atributosSolo_EDIT','listas_edit',1,'p_listaFilesEDIT','main.py',1047),
  ('atributosSolo_EDIT -> GUION PATH DIR','atributosSolo_EDIT',3,'p_atributoSolo_EDIT','main.py',1055),
  ('atributosSolo_EDIT -> GUION CONT DIR','atributosSolo_EDIT',3,'p_atributoSolo_EDIT','main.py',1056),
  ('comando -> RENAME lista_rename','comando',2,'p_comando_rename','main.py',1063),
  ('lista_rename -> lista_rename atributosSolo_RENAME','lista_rename',2,'p_listaFilesRENAME','main.py',1090),
  ('lista_rename -> atributosSolo_RENAME','lista_rename',1,'p_listaFilesRENAME','main.py',1091),
  ('atributosSolo_RENAME -> GUION PATH DIR','atributosSolo_RENAME',3,'p_atributoSolo_RENAME','main.py',1099),
  ('atributosSolo_RENAME -> GUION NAME STRING','atributosSolo_RENAME',3,'p_atributoSolo_RENAME','main.py',1100),
  ('comando -> MKDIR lista_mkdir','comando',2,'p_comando_mkdir','main.py',1107),
  ('lista_mkdir -> lista_mkdir atributosSolo_MKDIR','lista_mkdir',2,'p_listaFilesMKDIR','main.py',1142),
  ('lista_mkdir -> atributosSolo_MKDIR','lista_mkdir',1,'p_listaFilesMKDIR','main.py',1143),
  ('atributosSolo_MKDIR -> GUION PATH DIR','atributosSolo_MKDIR',3,'p_atributoSolo_MKDIR','main.py',1151),
  ('atributosSolo_MKDIR -> GUION R','atributosSolo_MKDIR',2,'p_atributoSolo_MKDIR','main.py',1152),
  ('comando -> COPY lista_copy','comando',2,'p_comando_copy','main.py',1162),
  ('lista_copy -> lista_copy atributosSolo_COPY','lista_copy',2,'p_listaFilesCOPY','main.py',1190),
  ('lista_copy -> atributosSolo_COPY','lista_copy',1,'p_listaFilesCOPY','main.py',1191),
  ('atributosSolo_COPY -> GUION PATH DIR','atributosSolo_COPY',3,'p_atributoSolo_COPY','main.py',1199),
  ('atributosSolo_COPY -> GUION DESTINO DIR','atributosSolo_COPY',3,'p_atributoSolo_COPY','main.py',1200),
  ('comando -> EXECUTE GUION PATH DIR','comando',4,'p_comando_execute','main.py',1207),
  ('comando -> REP lista_rep','comando',2,'p_comando_rep','main.py',1230),
  ('lista_rep -> lista_rep atributosSolo_REP','lista_rep',2,'p_listaFilesREP','main.py',1392),
  ('lista_rep -> atributosSolo_REP','lista_rep',1,'p_listaFilesREP','main.py',1393),
  ('atributosSolo_REP -> GUION ID STRING','atributosSolo_REP',3,'p_atributoSolo_REP','main.py',1401),
  ('atributosSolo_REP -> GUION PATH DIR','atributosSolo_REP',3,'p_atributoSolo_REP','main.py',1402),
  ('atributosSolo_REP -> GUION NAME STRING','atributosSolo_REP',3,'p_atributoSolo_REP','main.py',1403),
  ('atributosSolo_REP -> GUION RUTA DIR','atributosSolo_REP',3,'p_atributoSolo_REP','main.py',1404),
  ('comando -> PAUSE','comando',1,'p_comando_pause','main.py',1408),
]
