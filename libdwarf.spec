%global major 1
%define libname %mklibname dwarf %{major}
%define devname %mklibname -d dwarf
%define soversion %{major}
%define soname libdwarf.so.%{soversion}
%define sofullname libdwarf.so.%{soversion}.%{version}.0
%define _disable_lto 1
%define _disable_ld_no_undefined 1

Name:		libdwarf
Version:	20200114
Release:	1
Summary:	Library to access the DWARF Debugging file format
Group:		Development/C
License:	LGPLv2
URL:		http://www.prevanders.net/dwarf.html
Source0:	http://www.prevanders.net/%{name}-%{version}.tar.gz
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
install -pDm 0644 libdwarf/dwarf.h %{buildroot}%{_includedir}/libdwarf/dwarf.h
install -pDm 0644 libdwarf/.libs/libdwarf.a %{buildroot}%{_libdir}/libdwarf.a
install -pDm 0644 libdwarf/libdwarf.h %{buildroot}%{_includedir}/libdwarf/libdwarf.h
install -pDm 0755 libdwarf/.libs/libdwarf.so %{buildroot}%{_libdir}/%{sofullname}
ln -s %{sofullname} %{buildroot}%{_libdir}/%{soname}
ln -s %{sofullname} %{buildroot}%{_libdir}/libdwarf.so
install -pDm 0755 dwarfdump/dwarfdump %{buildroot}%{_bindir}/dwarfdump

%files -n %{libname}
%{_libdir}/libdwarf.so.%{major}
%{_libdir}/libdwarf.so.%{major}.*

%files static
%{_libdir}/libdwarf.a

%files -n %{devname}
%doc libdwarf/*.pdf
%doc dwarfdump/README dwarfdump/ChangeLog
%doc dwarfdump/COPYING dwarfdump/DWARFDUMPCOPYRIGHT dwarfdump/GPL.txt
%{_includedir}/libdwarf
%{_libdir}/libdwarf.so

%files tools
%{_bindir}/dwarfdump
