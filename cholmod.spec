%define epoch		0

%define name		cholmod
%define NAME		CHOLMOD
%define version		1.6.0
%define release		%mkrel 3
%define major		%{version}
%define libname		%mklibname %{name} %{major}
%define develname	%mklibname %{name} -d

%define enable_metis 	0

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Routines for factorizing sparse symmetric positive definite matricies
Group:		System/Libraries
License:	LGPL
URL:		http://www.cise.ufl.edu/research/sparse/cholmod/
Source0:	http://www.cise.ufl.edu/research/sparse/cholmod/%{NAME}-%{version}.tar.gz
Source1:	http://www.cise.ufl.edu/research/sparse/ufconfig/UFconfig-3.1.0.tar.gz
BuildRequires:	blas-devel, lapack-devel
BuildRequires:	amd-devel >= 2.0.0, camd-devel >= 2.0.0
BuildRequires:	colamd-devel >= 2.0.0, ccolamd-devel >= 2.0.0
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description

%package -n %{libname}
Summary:	Library of routines for factorizing sparse symmetric positive definite matricies
Group:		System/Libraries
Provides:	%{libname} = %{epoch}:%{version}-%{release}
Obsoletes:	%mklibname %name 1

%description -n %{libname}

This package contains the library needed to run programs dynamically
linked against %{NAME}.

%package -n %{develname}
Summary:	C routines for factorizing sparse symmetric positive definite matricies
Group:		Development/C
Requires:	suitesparse-common-devel >= 3.0.0
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes: 	%mklibname %name 1 -d
Obsoletes: 	%mklibname %name 1 -d -s

%description -n %{develname}
CHOLMOD is a set of routines for factorizing sparse symmetric positive
definite matrices of the form A or AA', updating/downdating a
sparse Cholesky factorization, solving linear systems,
updating/downdating the solution to the triangular system Lx=b,
and many other sparse matrix functions for both symmetric and
unsymmetric matrices.  Its supernodal Cholesky factorization
relies on LAPACK and the Level-3 BLAS, and obtains a substantial
fraction of the peak performance of the BLAS.  Both real and
complex matrices are supported.

This package contains the files needed to develop applications which
use %{name}.

%prep
%setup -q -c 
%setup -q -c -a 0 -a 1
%setup -q -D -T -n %{name}-%{version}/%{NAME}

%build
%if "%{?enable_metis}" == "1"
CHOLMOD_FLAGS="%{optflags} -I%{_includedir}/metis -fPIC"
%else
CHOLMOD_FLAGS="%{optflags} -DNPARTITION -fPIC"
%endif
pushd Lib
    %make -f Makefile CC=%__cc CFLAGS="$RPM_OPT_FLAGS $CHOLMOD_FLAGS -fPIC -I/usr/include/suitesparse" INC=
    %__cc -shared -Wl,-soname,lib%{name}.so.%{major} -o lib%{name}.so.%{version} -lamd -lcamd -lcolamd -lccolamd -lm *.o
popd

%install
%__rm -rf %{buildroot}

%__install -d -m 755 %{buildroot}%{_libdir} 
%__install -d -m 755 %{buildroot}%{_includedir}/suitesparse 

for f in Lib/*.so*; do
    %__install -m 755 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Lib/*.a; do
    %__install -m 644 $f %{buildroot}%{_libdir}/`basename $f`
done
for f in Include/*.h; do
    %__install -m 644 $f %{buildroot}%{_includedir}/suitesparse/`basename $f`
done

%__ln_s lib%{name}.so.%{version} %{buildroot}%{_libdir}/lib%{name}.so

%__install -d -m 755 %{buildroot}%{_docdir}/%{name}
%__install -m 644 README.txt Core/*.txt Doc/*.pdf Doc/ChangeLog %{buildroot}%{_docdir}/%{name}

%clean
%__rm -rf %{buildroot}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%files -n %{libname}
%defattr(-,root,root)
%{_docdir}/%{name}
%{_libdir}/*.so.*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
