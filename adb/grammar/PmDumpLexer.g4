lexer grammar PmDumpLexer;

ID              : [a-f0-9]+ ; // 16 进制 ID
FULL_CLASS_PATH : [a-zA-Z0-9_./]+ ;
STRING_LITERAL  : '"' .*? '"' ;
WS              : [ \t\r\n]+ -> skip ;