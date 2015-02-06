%define reldate	20111214
%define	major	0
%define	libname	%mklibname dwarf 0
%define	devname	%mklibname -d dwarf
%define	static	%mklibname -d -s dwarf

Summary:	Library to access the DWARF Debugging file format 
Name:		libdwarf
Version:	0.%{reldate}
Release:	2
License:	LGPLv2
Group:		System/Libraries
URL:		http://reality.sgiweb.org/davea/dwarf.html
Source0:	http://reality.sgiweb.org/davea/%{name}-%{reldate}.tar.gz
# This patch set up the proper soname
Patch0:		libdwarf-soname-fix.patch
Patch1:		dwarf-20111030-link-against-required-libelf.patch
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
Provides:	dwarf-devel = %{EVRD}

%description -n	%{devname}
Development package containing library and header files of libdwarf.

%package -n	%{static}
Summary:	Static libdwarf library
Group:		Development/C
Requires:	%{devname} = %{EVRD}
Provides:	dwarf-static-devel = %{EVRD}

%description -n	%{static}
Static libdwarf library.

%package -n	dwarf-tools
Summary:	Tools for accessing DWARF debugging information
License:	GPLv2
Group:		Development/Other

%description -n	dwarf-tools
C++ version of dwarfdump (dwarfdump2) command-line utilities 
to access DWARF debug information.

%prep
%setup -q -n dwarf-%{reldate}
%patch0 -p1 -b .soname-fix~
%patch1 -p1 -b .libelf~
find |xargs chmod o+r

%build
pushd libdwarf
%configure2_5x --enable-shared
%make
popd

# Need to also configure dwarfdump since dwarfdump2 Makefile 
# depends on dwarfdump's Makefile
pushd dwarfdump
%configure2_5x
popd

pushd dwarfdump2
%configure2_5x
LD_LIBRARY_PATH="../libdwarf" make
popd

%install
install -pm755 libdwarf/libdwarf.so.%{major}.0 -D %{buildroot}%{_libdir}/libdwarf.so.%{major}.0
cp -pd libdwarf/libdwarf.so.%{major}	   %{buildroot}%{_libdir}/libdwarf.so.%{major}
cp -pd libdwarf/libdwarf.so.%{major}	   %{buildroot}%{_libdir}/libdwarf.so

install -pm644 libdwarf/libdwarf.a	-D %{buildroot}%{_libdir}/libdwarf.a
install -pm644 libdwarf/dwarf.h		-D %{buildroot}%{_includedir}/libdwarf/dwarf.h
install -pm644 libdwarf/libdwarf.h	-D %{buildroot}%{_includedir}/libdwarf/libdwarf.h

install -pm755 dwarfdump2/dwarfdump	-D %{buildroot}%{_bindir}/dwarfdump

%files -n	%{libname}
%doc libdwarf/ChangeLog libdwarf/README libdwarf/COPYING libdwarf/LIBDWARFCOPYRIGHT
%{_libdir}/libdwarf.so.0*

%files -n	%{devname}
%doc libdwarf/*.pdf
%dir %{_includedir}/libdwarf
%{_includedir}/libdwarf/dwarf.h
%{_includedir}/libdwarf/libdwarf.h
%{_libdir}/libdwarf.so

%files -n	%{static}
%{_libdir}/libdwarf.a

%files	-n	dwarf-tools
%doc dwarfdump2/README dwarfdump2/ChangeLog dwarfdump2/COPYING dwarfdump2/DWARFDUMPCOPYRIGHT
%{_bindir}/dwarfdump


%changelog
* Tue Dec 20 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.20111214-1
+ Revision: 743929
- fix group
- new version
- make all files world readable
- parallel build for dwarfdump2 turned out to not be reliable after all...
- drop LGPL.txt as well as it's provided by 'common-licenses'
- rename libdwarf-tools package to dwarf-tools
- add canonical provides for devel packages
- be sure to link against libelf (P1)
- improve soname patch
- parallel build for dwarfdump2 seems to be working again..
- don't have to pass CFLAGS manually, it's already done by configure
- drop GPL.txt as the license is provided by 'common-licenses'
- imported package libdwarf


* Mon Nov 28 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.20111030-1
- 20111030 release adapted from Fedora package

* Wed Jul 13 2011 Parag Nemade <paragn AT fedoraproject DOT org> - 0.20110612-1
- Update to 20110612 release

* Wed Mar 09 2011 Parag Nemade <paragn AT fedoraproject DOT org> - 0.20110113-1
- Update to 20110113 release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100629-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 06 2010 Parag Nemade <paragn AT fedoraproject.org> - 0.20100629-1
- Update to 20100629 release
- Add -static subpackage as request in rh#586807

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090324-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 31 2009 - Suravee Suthikulpanit <suravee.suthikulpanit@amd.com>
- 0.20090324-4
- Adding _smp_mflags for libdwarf build
- Move CFLAGS override from configure to make
 
* Mon Mar 30 2009 - Suravee Suthikulpanit <suravee.suthikulpanit@amd.com>
- 0.20090324-3
- Remove AutoreqProv no

* Thu Mar 26 2009 - Suravee Suthikulpanit <suravee.suthikulpanit@amd.com>
- 0.20090324-2
- Drop the C implementation of dwarfdump. (dwarfdump1)
- Since the doc package is small, we combined the contents into the devel package.
- Fix the version string.
- Drop the static library.
- Add release number to "Requires".
- Fix licensing (v2 instead of v2+)
- Change linking for libdwarf.so and libdwarf.so.0

* Wed Mar 25 2009 - Suravee Suthikulpanit <suravee.suthikulpanit@amd.com>
- 20090324-1
- Initial Revision
