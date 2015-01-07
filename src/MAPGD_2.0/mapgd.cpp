#include <iostream>
#include <cstdio>
#include <cstring>

#include "interface.h"
#include "proview.h"
#include "comparePooled.h"
#include "estimatePooled.h"

using namespace std;

/** @brief Our main function.
  * Parses commandline arguments etc.
  * @returns 0 iff seccessful
**/
int main (int argc, char* argv[])
{
	env_t env;
	env.setname("mapgd");
	env.setver("1.0");
	env.setauthor("Matthew Ackerman");
	env.setdescription("A program for maximum-likelihood analysis of population genomic data");

	env.flag(	'h',"help", 	&env, 		&flag_help, 	"an error occured while displaying the help message", "prints this message");
	env.flag(	'v',"version", 	&env, 		&flag_version, 	"an error occured while displaying the version message", "prints the program version");

	env.command(	' ',"proview", 	&proview, 			"an error occured while calling proview", "prints data in the '.pro' file quartet format");
	env.command(	' ',"ep", 	&estimatePooled, 		"an error occured while calling ep", "estimates allele frequencies using pooled data");
	env.command(	' ',"cp", 	&comparePooled, 		"an error occured while calling cp", "compares allele frequencies between populations using pooled data");

//	env.command(	' ',"ci", 	&compareIndividual, 		"an error occured while calling ci", "compares allele frequencines between population using indivdual data ");
//	env.command(	' ',"ei", 	&estimateIndividual, 		"an error occured while calling ei", "estimates allelel frequencies using individual data");
//	env.command(	' ',"ri", 	&RelationshipIndividual, 	"an error occured while calling ri", "estimates the relationship betweem two individuals in a population");

//	env.command(	' ',"eq", 	&estimateQuality, 		"an error occured while calling eq", "estimates error rate as a function of illumina quality score");

	if ( parsargs(argc, argv, env) ) printUsage(env);

	printUsage(env);

	exit(0);
}
