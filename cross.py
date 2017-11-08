#!/usr/bin/python
# -*- coding: utf-8 -*-

from scipy import stats

if __name__ == "__main__":
	dec = [0.603, 0.577, 0.588, 0.591, 0.601, 0.621, 0.584, 0.580, 0.564, 0.575]
	bay = [0.616, 0.611, 0.598, 0.609, 0.595, 0.648, 0.590, 0.600, 0.589, 0.594]
	svm = [0.632, 0.628, 0.634, 0.645, 0.612, 0.663, 0.621, 0.620, 0.610, 0.616]

	print stats.ttest_rel(dec, bay)
	print stats.ttest_rel(svm, bay)
	print stats.ttest_rel(dec, svm)