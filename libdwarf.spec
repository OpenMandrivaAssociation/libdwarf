%global major 0
%define libname %mklibname dwarf %{major}
%define devname %mklibname -d dwarf
%define soversion %{major}
%define soname libdwarf.so.%{soversion}
%define sofullname libdwarf.so.%{soversion}.%{version}.0
%define _disable_lto 1
%define _disable_ld_no_undefined 1

Name:		libdwarf
Version:	0.8.0
Release:	1
Summary:	Library to access the DWARF Debugging file format
Group:		Development/C
License:	LGPLv2
URL:		http://www.prevanders.net/dwarf.html
Source0:	https://www.prevanders.net/libdwarf-%{version}.tar.xz
BuildRequires:	binutils-devel
BuildRequires:	elfutils-devel

%package -n %{libname}
Summary:	Library files of libdwarf
Group:		System/Libraries

%description -n %{libname}
Library to access the DWARF debugging file format which supports
source level debugging of a number of procedural languages, such as C, C++,
and Fortran.  Please see http://www.dwarfstd.org for DWARF specification.

%package -n %{devname}
Summary:	Library and header files of libdwarf
Group:		Development/C
License:	LGPLv2
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%package static
Summary:	Static libdwarf library
Group:		Development/C
License:	LGPLv2
Requires:	%{name}-devel = %{version}-%{release}

%package tools
Summary:	Tools for accessing DWARF debugging information
Group:		Development/Tools
License:	GPLv2
Requires:	%{libname} = %{version}-%{release}

%description
Library to access the DWARF debugging file format which supports
source level debugging of a number of procedural languages, such as C, C++,
and Fortran.  Please see http://www.dwarfstd.org for DWARF specification.

%description static
Static libdwarf library.

%description -n %{devname}
Development package containing library and header files of libdwarf.

%description tools
C++ version of dwarfdump (dwarfdump2) command-line utilities
to access DWARF debug information.

%prep
%setup -qn %{name}-%{version}
%autopatch -p1

%build
%configure --enable-shared --enable-static
LD_LIBRARY_PATH="../libdwarf" %make SONAME="%{soname}"

%install
%make_install
mkdir %{buildroot}%{_includedir}/libdwarf
cp -l %{buildroot}%{_includedir}/libdwarf-0/*.h %{buildroot}%{_includedir}/libdwarf

%files -n %{libname}
%{_libdir}/libdwarf.so.%{major}
%{_libdir}/libdwarf.so.%{major}.*

%files static
%{_libdir}/libdwarf.a

%files -n %{devname}
%{_includedir}/libdwarf-%{major}/
%{_includedir}/libdwarf/
%{_libdir}/libdwarf.so
%{_libdir}/pkgconfig/libdwarf.pc

%files tools
%{_bindir}/dwarfdump
%{_datadir}/dwarfdump/dwarfdump.conf
%{_mandir}/man1/dwarfdump.1.*
