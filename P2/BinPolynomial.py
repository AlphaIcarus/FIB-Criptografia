#Copyright (c) 2013 Anisimov Nikita <ravis.bmstu at gmail dot com>

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#documentation files (the "Software"), to deal in the Software without restriction, including without limitation
#the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
#to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
#the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
#THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
#TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

def optiSizeVec(vec):
	optiVec=[]
	if len(vec)==0:
		return optiVec
	if len(vec)==1:
		if vec[0]==1:
			return vec
		else:
			return optiVec
	for i in range(1,len(vec)+1):
		if vec[-i]==0:
			continue
		else:
			for j in range(-len(vec),-i+1):
				optiVec.append(vec[j])
			break;
	return optiVec

def BinPolySum(b1,b2):
	result=[]
	shortest=None
	longest=None
	if (len(b1)==len(b2)):
		for i in range(0,len(b1)):
			result.append((int(b1[i])+int(b2[i]))%2)
		result=optiSizeVec(result)
		return result
	elif (len(b1)>len(b2)):
		shortest=b2
		longest=b1
	else:
		shortest=b1
		longest=b2
	for i in range(0,len(shortest)):
		result.append((b1[i]+b2[i])%2)
	for j in range(len(shortest),len(longest)):
		result.append(longest[j])
	result=optiSizeVec(result)
	return result

def BinPolyMul(b1,b2):
	result=[]
	for i in range(0,len(b1)+len(b2)-1):
		result.append(0)
	for i in range(0,len(b1)):
		if b1[i]==0:
			continue;
		for j in range(0,len(b2)):
			if b2[j]==0:
				continue
			sumDegree=i+j
			result[sumDegree]=1
	result=optiSizeVec(result)
	return result

def BinPolyDiv(b1,b2):
	quotient=[]
	for i in range(0,len(b1)):
		quotient.append(0)
	remainder=b1
	while (len(remainder)>=len(b2)):
		# print 'Iteration'
		dividendDegree=len(remainder)-1
		dividerDegree=len(b2)-1
		degreeDelta=dividendDegree-dividerDegree
		quotient[degreeDelta]=1
		subQuotient=[]
		for i in range(0,degreeDelta+1):
			if i==degreeDelta:
				subQuotient.append(1)
			else:
				subQuotient.append(0)
		summer=BinPolyMul(b2,subQuotient)
		# print 'quotient = '+str(quotient)
		# print 'subQuotient = '+str(subQuotient)
		# print 'summer = '+str(summer)
		# print 'before sum remainder = '+str(remainder)
		remainder=BinPolySum(remainder,summer)
		# print 'before optiSizeVec remainder = '+str(remainder)
		remainder=optiSizeVec(remainder)
		# print 'remainder = '+str(remainder)
	quotient=optiSizeVec(quotient)
	remainder=optiSizeVec(remainder)
	return (quotient,remainder)