%define NAME	CHOLMOD
%define major	2
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

%bcond_without	metis

Name:		cholmod
Version:	2.1.2
Release:	9
Epoch:		1
Summary:	Routines for factorizing sparse symmetric positive definite matricies
Group:		System/Libraries
License:	LGPLv2+
URL:		http://www.cise.ufl.edu/research/sparse/cholmod/
Source0:	http://www.cise.ufl.edu/research/sparse/cholmod/%{NAME}-%{version}.tar.gz
Patch0:		cholmod-2.1.2-no-cuda.patch
Patch1:		cholmod-2.1.2-metis5-support.patch
BuildRequires:	blas-devel
BuildRequires:	lapack-devel
BuildRequires:	amd-devel >= 2.0.0
BuildRequires:	camd-devel >= 2.0.0
BuildRequires:	colamd-devel >= 2.0.0
BuildRequires:	ccolamd-devel >= 2.0.0
BuildRequires:	suitesparseconfig-devel >= 4.2.1-3
%if %{with metis}
BuildRequires:	metis-devel >= 5.1.0
%endif

%description
CHOLMOD is a set of routines for factorizing sparse symmetric positive
definite matrices of the form A or AA', updating/downdating a sparse
Cholesky factorization, solving linear systems, updating/downdating
the solution to the triangular system Lx=b, and many other sparse
matrix functions for both symmetric and unsymmetric matrices.  Its
supernodal Cholesky factorization relies on LAPACK and the Level-3
BLAS, and obtains a substantial fraction of the peak performance of
the BLAS.  Both real and complex matrices are supported.

%package -n %{libname}
Summary:	Routines for factorizing sparse symmetric positive definite matricies
Group:		System/Libraries

%description -n %{libname}
CHOLMOD is a set of routines for factorizing sparse symmetric positive
definite matrices of the form A or AA', updating/downdating a sparse
Cholesky factorization, solving linear systems, updating/downdating
the solution to the triangular system Lx=b, and many other sparse
matrix functions for both symmetric and unsymmetric matrices.  Its
supernodal Cholesky factorization relies on LAPACK and the Level-3
BLAS, and obtains a substantial fraction of the peak performance of
the BLAS.  Both real and complex matrices are supported.

This package contains the library needed to run programs dynamically
linked against %{NAME}.

%package -n %{devname}
Summary:	C routines for factorizing sparse symmetric positive definite matricies
Group:		Development/C
Requires:	suitesparse-common-devel >= 4.0.0
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
CHOLMOD is a set of routines for factorizing sparse symmetric positive
definite matrices of the form A or AA', updating/downdating a sparse
Cholesky factorization, solving linear systems, updating/downdating
the solution to the triangular system Lx=b, and many other sparse
matrix functions for both symmetric and unsymmetric matrices.  Its
supernodal Cholesky factorization relies on LAPACK and the Level-3
BLAS, and obtains a substantial fraction of the peak performance of
the BLAS.  Both real and complex matrices are supported.

This package contains the files needed to develop applications which
use %{name}.

%prep
%setup -q -c -n %{name}-%{version}
%patch0 -p1 -b .nocuda~
%patch1 -p1 -b .metis5~

cd %{NAME}
find . -perm 0600 | xargs chmod 0644
mkdir ../SuiteSparse_config
ln -sf %{_includedir}/suitesparse/SuiteSparse_config.* ../SuiteSparse_config

%build
cd %{NAME}
%if %{with metis}
CONF=""
%else
CONF="-DNPARTITION"
%endif
pushd Lib
    %make CC=gcc CONFIG="$CONF" CFLAGS="%{optflags} -I%{_includedir}/suitesparse" INC=
    gcc %{ldflags} -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} *.o -lsuitesparseconfig -lamd -lcamd -lcolamd -lccolamd -lblas -llapack -lm \
%if %{with metis}
    -lmetis
%endif

popd

%install
cd %{NAME}

for f in Lib/*.so*; do
    install -m755 $f -D %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    install -m644 $f -D %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    install -m644 $f -D %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

ln -s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

install -d -m 755 %{buildroot}%{_docdir}/%{name}
install -m 644 README.txt Core/*.txt Doc/*.pdf Doc/ChangeLog %{buildroot}%{_docdir}/%{name}

%files -n %{libname}
%{_libdir}/libcholmod.so.%{major}*

%files -n %{devname}
%{_docdir}/%{name}
%{_includedir}/*
%{_libdir}/libcholmod.so
%{_libdir}/libcholmod.a
