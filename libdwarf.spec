%define reldate	20111030
%define	major	0
%define	libname	%mklibname dwarf 0
%define	devname	%mklibname -d dwarf
%define	static	%mklibname -d -s dwarf

Summary:	Library to access the DWARF Debugging file format 
Name:		libdwarf
Version:	0.%{reldate}
Release:	1
License:	LGPLv2
Group:		System/Libraries
URL:		http://reality.sgiweb.org/davea/dwarf.html
Source0:	http://reality.sgiweb.org/davea/%{name}-%{reldate}.tar.gz
# This patch set up the proper soname
Patch0:		libdwarf-soname-fix.patch
BuildRequires:	binutils-devel elfutils-devel

%description
Library to access the DWARF debugging file format which supports
source level debugging of a number of procedural languages, such as C, C++,
and Fortran.  Please see http://www.dwarfstd.org for DWARF specification.

%package -n	%{libname}
Summary:	Library to access the DWARF Debugging file format 
Group:		System/Libraries

%description -n	%{libname}
Library to access the DWARF debugging file format which supports
source level debugging of a number of procedural languages, such as C, C++,
and Fortran.  Please see http://www.dwarfstd.org for DWARF specification.

%package -n	%{devname}
Summary:	Library and header files of libdwarf
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n	%{devname}
Development package containing library and header files of libdwarf.

%package -n	%{static}
Summary:	Static libdwarf library
Group:		Development/C
Requires:	%{devname} = %{EVRD}

%description -n	%{static}
Static libdwarf library.

%package	tools
Summary:	Tools for accessing DWARF debugging information
License:	GPLv2
Group:		Development/Tools

%description	tools
C++ version of dwarfdump (dwarfdump2) command-line utilities 
to access DWARF debug information.

%prep
%setup -q -n dwarf-%{reldate}
%patch0 -p0 -b .soname-fix

%build
pushd libdwarf
%configure --enable-shared
%make libdwarf.so.0.0 libdwarf.a 
ln -s libdwarf.so.0.0 libdwarf.so
ln -s libdwarf.so.0.0 libdwarf.so.0
popd

# Need to also configure dwarfdump since dwarfdump2 Makefile 
# depends on dwarfdump's Makefile
pushd dwarfdump
%configure 
popd

pushd dwarfdump2
%configure 
# Note: %{?_smp_mflags} failed to build
LD_LIBRARY_PATH="../libdwarf" make all
popd

%install
install -pm755 libdwarf/libdwarf.so.0.0 -D %{buildroot}%{_libdir}/libdwarf.so.%{major}.0
ln -s libdwarf.so.%{major}.0		   %{buildroot}%{_libdir}/libdwarf.so.%{major}
ln -s libdwarf.so.%{major}		   %{buildroot}%{_libdir}/libdwarf.so

install -pm644 libdwarf/libdwarf.a	-D %{buildroot}%{_libdir}/libdwarf.a
install -pm644 libdwarf/dwarf.h		-D %{buildroot}%{_includedir}/libdwarf/dwarf.h
install -pm644 libdwarf/libdwarf.h	-D %{buildroot}%{_includedir}/libdwarf/libdwarf.h

install -pm755 dwarfdump2/dwarfdump	-D %{buildroot}%{_bindir}/dwarfdump

%files -n	%{libname}
%doc libdwarf/ChangeLog libdwarf/README libdwarf/COPYING libdwarf/LIBDWARFCOPYRIGHT libdwarf/LGPL.txt
%{_libdir}/libdwarf.so.0*

%files -n	%{devname}
%doc libdwarf/*.pdf
%dir %{_includedir}/libdwarf
%{_includedir}/libdwarf/dwarf.h
%{_includedir}/libdwarf/libdwarf.h
%{_libdir}/libdwarf.so

%files -n	%{static}
%{_libdir}/libdwarf.a

%files		tools
%doc dwarfdump2/README dwarfdump2/ChangeLog dwarfdump2/COPYING dwarfdump2/DWARFDUMPCOPYRIGHT
%{_bindir}/dwarfdump

