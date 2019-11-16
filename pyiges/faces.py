"""
Face (Type 510)
Defines a bound portion of three dimensional space (R^3) which has a
finite area. Used to construct B-Rep Geometries.

Parameter Data
Index in list	Type of data	Name	Description
Pointer	Surface	Underlying surface
2	INT	N	Number of loops
3	BOOL	Flag	Outer loop flag:
True indicates Loop1 is outer loop.
False indicates no outer loop.
4	Pointer	Loop1	Pointer to first loop of the face
.
.	.
.	.
.	
3+N	Pointer	LoopN	Pointer to last loop of the face
"""

