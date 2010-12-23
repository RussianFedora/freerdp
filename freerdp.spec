Name:           freerdp
Version:        0.8.1
Release:        1%{?dist}
Summary:        Remote Desktop Protocol client

Group:          Applications/Communications
License:        GPLv2+
URL:            http://www.freerdp.com/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  alsa-lib-devel
BuildRequires:  cups-devel
BuildRequires:  openssl-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel

Provides:       xfreerdp = %{version}-%{release}
Requires:       %{name}-libs = %{version}-%{release}, %{name}-plugins = %{version}-%{release}

%description 
The xfreerdp Remote Desktop Protocol (RDP) client from the FreeRDP
project.

xfreerdp can connect to RDP servers such as Microsoft Windows
machines, xrdp and VirtualBox.

FreeRDP is a fork of the rdesktop project and intends to rapidly
improve on it and re-implement what is needed.


%package        libs
Summary:        Core libraries implementing the RDP protocol
Group:          System Environment/Libraries
%description    libs
libfreerdp implements the core of the RDP protocol.

libfreerdpchanman can be used to load plugins that can handle channels
in the RDP protocol.

libfreerdpkbd implements functionality for handling keyboards in X.


%package        plugins
Summary:        Plugins for handling the standard RDP channels
Group:          System Environment/Libraries
Requires:       %{name}-libs = %{version}-%{release}
%description    plugins
A set of plugins to the channel manager implementing the standard virtual
channels extending RDP core functionality.  For example, sounds, clipboard
sync, disk/printer redirection, etc.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}-libs.


%prep
%setup -q


%build
%configure --disable-static --with-sound=alsa --with-crypto=openssl
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_bindir}/xfreerdp
%{_mandir}/*/*

%files libs
%defattr(-,root,root,-)
%doc COPYING AUTHORS doc/ipv6.txt
%{_libdir}/*.so.*
%dir %{_libdir}/%{name}/
%{_datadir}/%{name}/

%files plugins
%defattr(-,root,root,-)
%{_libdir}/%{name}/*.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Wed Oct 27 2010 Arkady L. Shjane <ashejn@yandex-team.ru> - 0.8.1-1
- update to 0.8.1

* Sat Sep 25 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.4-2
- hack the generated libtool to not set rpath on x86_64
- configure with alsa explicitly

* Tue Aug 24 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.4-1
- freerdp-0.7.4
- cleanup of packaging structure

* Wed Jul 28 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.3-1
- 0.7.3
- fix some minor pylint warnings

* Fri Jul 23 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.2-2
- 0.7.2
- Address many comments from cwickert:
- - cleanup of old formatting, alignment with spectemplate-lib.spec and
    cwickert spec from #616193
- - add alsa as build requirement
- - remove superfluous configure options and disable static libs
- - add missing rpm groups

* Sun Jun 13 2010 Mads Kiilerich <mads@kiilerich.com> - 0.7.0-1
- First official release, first review request
