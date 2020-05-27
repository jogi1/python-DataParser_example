typedef unsigned long u_long;

typedef struct                 // A Directory entry
{ long  offset;                // Offset to entry, in bytes, from start of file
  long  size;                  // Size of entry in file, in bytes
} dentry_t;

typedef struct                 // The BSP file header
{ long  version;               // Model version, must be 0x17 (23).
  dentry_t entities;           // List of Entities.
  dentry_t planes;             // Map Planes.
                               // numplanes = size/sizeof(plane_t)
  dentry_t miptex;             // Wall Textures.
  dentry_t vertices;           // Map Vertices.
                               // numvertices = size/sizeof(vertex_t)
  dentry_t visilist;           // Leaves Visibility lists.
  dentry_t nodes;              // BSP Nodes.
                               // numnodes = size/sizeof(node_t)
  dentry_t texinfo;            // Texture Info for faces.
                               // numtexinfo = size/sizeof(texinfo_t)
  dentry_t faces;              // Faces of each surface.
                               // numfaces = size/sizeof(face_t)
  dentry_t lightmaps;          // Wall Light Maps.
  dentry_t clipnodes;          // clip nodes, for Models.
                               // numclips = size/sizeof(clipnode_t)
  dentry_t leaves;             // BSP Leaves.
                               // numlaves = size/sizeof(leaf_t)
  dentry_t lface;              // List of Faces.
  dentry_t edges;              // Edges of faces.
                               // numedges = Size/sizeof(edge_t)
  dentry_t ledges;             // List of Edges.
  dentry_t models;             // List of Models.
                               // nummodels = Size/sizeof(model_t)
} dheader_t;

typedef float scalar_t;        // Scalar value,

typedef struct                 // Vector or Position
{ scalar_t x;                  // horizontal
  scalar_t y;                  // horizontal
  scalar_t z;                  // vertical
} vec3_t;

typedef struct                 // Bounding Box, Float values
{ vec3_t   min;                // minimum values of X,Y,Z
  vec3_t   max;                // maximum values of X,Y,Z
} boundbox_t;

typedef struct                 // Bounding Box, Short values
{ short   min;                 // minimum values of X,Y,Z
  short   max;                 // maximum values of X,Y,Z
} bboxshort_t;

typedef struct                 // Mip texture list header
{ long numtex;                 // Number of textures in Mip Texture list
  long offset[];         // Offset to each of the individual texture DataParser={'array_length_reference': 'numtex'}
} mipheader_t;                 //  from the beginning of mipheader_t

typedef struct                 // Mip Texture
{ char   name[16];             // Name of the texture.
  u_long width;                // width of picture, must be a multiple of 8
  u_long height;               // height of picture, must be a multiple of 8
  u_long offset1;              // offset to u_char Pix[width   * height]
  u_long offset2;              // offset to u_char Pix[width/2 * height/2]
  u_long offset4;              // offset to u_char Pix[width/4 * height/4]
  u_long offset8;              // offset to u_char Pix[width/8 * height/8]
} miptex_t;
