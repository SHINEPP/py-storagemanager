parser grammar PmDumpParser;

options {
    tokenVocab = PmDumpLexer;
}

dump                    : 'DUMP OF SERVICE' 'package:' activityResolverTable ;
activityResolverTable   : 'Activity Resolver Table:' nonDataActions ;
nonDataActions          : 'Non-Data Actions:' actionEntry+ ;
actionEntry             : action ':' activityEntry ;
activityEntry           : ID FULL_CLASS_PATH 'filter' ID actionDetails ;
actionDetails           : ('Action:' STRING_LITERAL)? ('Category:' STRING_LITERAL)? ;

