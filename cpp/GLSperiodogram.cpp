// This is my first try with C++
#include <iostream>
#include <cmath>
/*#include "GLSperiodogram.h"*/

using namespace std;

#define PI 3.141519

extern "C" {
void GLS(double* prange, int nfreq, double* x, double* y, 
	 double* w, int ndata, double* gls)
  {
  double omega;
  double ccos, ssin;
  double Y, C, S;
  double YYhat, YChat, YShat, CChat, SShat, CShat;
  double YY, YC, YS, CC, SS, CS;
  double D;

  Y = 0;
  YYhat = 0;

  /* Sum where independent of frequency */
  for (int ii = 0; ii < ndata; ++ii)
    {
      Y += w[ii] * y[ii];
      YYhat += w[ii] * y[ii] * y[ii];
    }
    
  for (int jj = 0; jj < nfreq; ++jj)
    
    {
      omega = 2.0 * PI  / prange[jj];

      C = S = 0.0;
      YChat = YShat = CChat = SShat = CShat = 0.0;

      for (int ii = 0; ii < ndata; ++ii)
	{
	  ccos = cos(omega * x[ii]);			       
	  ssin = sin(omega * x[ii]);

	  C += w[ii] * ccos;
	  S += w[ii] * ssin;
      
	  YChat += w[ii] * y[ii] * ccos;
	  YShat += w[ii] * y[ii] * ssin;
	  CChat += w[ii] * ccos * ccos;
	  SShat += w[ii] * ssin * ssin;
	  CShat += w[ii] * ccos * ssin;
	}

      YY = YYhat - Y*Y;
      YC = YChat - Y*C;
      YS = YShat - Y*S;
      CC = CChat - C*C;
      SS = SShat - S*S;
      CS = CShat - C*S;

      D = CC*SS - CS*CS;
      
      gls[jj] = (SS * YC * YC + CC * YS * YS - 2.0 * CS * YC * YS) / (YY * D);
    }
  
    }
}

int main()
{
  cout << "OK\n";
  return 0;
  }
