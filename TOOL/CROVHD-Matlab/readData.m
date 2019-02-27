
% readData.m
% Reads and stores the data
function [a] = readData(datasetPath,outputpath)
%*************************************************************************

handles.plotFlag=0;                                     % density=1 or scatter=0 
handles.baseAxes=1;                                     % base axis for which scatter plot is drawn
handles.bitstr=0;

fid=fopen(datasetPath);
tline = fgetl(fid);
i=1;

while(length(tline)~=1 & length(tline) )
	tline
    C=textscan(tline, '%f %f %f %f %f', 'delimiter', ',', 'EmptyValue', 0);
    points(i,:)=double([C{1:4}]);
    i=i+1;
    tline = fgetl(fid);
end
handles.dimensions=4;
handles.colorDist=defaultColorDist(points,0.5);
distribution=ndimenl(4,points,0.5,5,0,handles,outputpath);
%distribution=ndimenl(4,points,1.5,5,0,handles,outputpath);
fclose(fid);
a=1;
end
%**************************************************************************
