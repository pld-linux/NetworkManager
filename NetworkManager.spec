# TODO:
# - add a working(!) pld backend... (it work's 4 me as it is now - czarny)
#
Summary:	Network Manager for GNOME
Summary(pl.UTF-8):	Zarządca sieci dla GNOME
Name:		NetworkManager
Version:	0.6.6
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://people.redhat.com/dcbw/NetworkManager/0.6.6/%{name}-%{version}.tar.gz
# Source0-md5:	412ed4db5d2db04285799c4303ddeeed
Source1:	%{name}.init
Source2:	%{name}Dispatcher.init
Patch0:		%{name}-pld.patch
BuildRequires:	GConf2-devel >= 2.20.0
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	gettext-devel
BuildRequires:	gnome-keyring-devel >= 2.20.0
BuildRequires:	gtk+2-devel >= 2:2.12.0
BuildRequires:	hal-devel >= 0.5.9
BuildRequires:	intltool >= 0.36.0
BuildRequires:	libgcrypt-devel
BuildRequires:	libgnomeui-devel >= 2.20.0
BuildRequires:	libglade2-devel >= 1:2.6.2
BuildRequires:	libiw-devel >= 1:28
BuildRequires:	libnl-devel >= 1:1.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dhcdbd
Requires:	libnl >= 1:1.1
Requires:	rc-scripts
Requires:	wpa_supplicant
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Network Manager for GNOME.

%description -l pl.UTF-8
Zarządca sieci dla GNOME.

%package libs
Summary:	Network Manager shared libraries
Summary(pl.UTF-8):	Biblioteki dzielone Network Managera
Group:		X11/Libraries
Conflicts:	NetworkManager < 0.6.4-0.2

%description libs
Network Manager shared libraries.

%description libs -l pl.UTF-8
Biblioteki dzielone Network Managera.

%package devel
Summary:	Network Manager includes and more
Summary(pl.UTF-8):	Pliki nagłówkowe Network Managera
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-glib-devel >= 0.72
Requires:	libgcrypt-devel

%description devel
Network Manager includes and more.

%description devel -l pl.UTF-8
Pliki nagłówkowe Network Manager.

%package static
Summary:	Network Manager static libraries
Summary(pl.UTF-8):	Statyczne biblioteki Network Managera
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Network Manager static libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Network Managera.

%prep
%setup -q
%patch0 -p1

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-distro=pld \
	--with-dhcdbd=%{_sbindir}/dhcdbd \
	--with-wpa_supplicant=%{_sbindir}/wpa_supplicant
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/run/%{name},%{_sysconfdir}/%{name}/dispatcher.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install test/nm-tool $RPM_BUILD_ROOT%{_bindir}/nm-tool

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/NetworkManager
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/NetworkManagerDispatcher


[ -d $RPM_BUILD_ROOT%{_datadir}/locale/sr@latin ] || \
	mv -f $RPM_BUILD_ROOT%{_datadir}/locale/sr@{Latn,latin}
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add NetworkManager
/sbin/chkconfig --add NetworkManagerDispatcher
%service NetworkManager restart "NetworkManager daemon"
%service NetworkManagerDispatcher restart "NetworkManagerDispatcher daemon"

%preun
if [ "$1" = "0" ]; then
	%service NetworkManager stop
	%service NetworkManagerDispatcher stop
	/sbin/chkconfig --del NetworkManager
	/sbin/chkconfig --del NetworkManagerDispatcher
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/nm-vpn-properties
%attr(755,root,root) %{_bindir}/nm-tool
%attr(755,root,root) %{_sbindir}/NetworkManager
%attr(755,root,root) %{_sbindir}/NetworkManagerDispatcher
%attr(755,root,root) %{_libdir}/nm-crash-logger
%attr(754,root,root) /etc/rc.d/init.d/NetworkManager
%attr(754,root,root) /etc/rc.d/init.d/NetworkManagerDispatcher
%dir %{_sysconfdir}/NetworkManager
%dir %{_sysconfdir}/NetworkManager/dispatcher.d
%dir %{_datadir}/%{name}
%dir /var/run/%{name}
%{_datadir}/gnome-vpn-properties
%{_datadir}/%{name}/gdb-cmd
%{_mandir}/man8/NetworkManager.8*
%{_mandir}/man8/NetworkManagerDispatcher.8*
%{_mandir}/man1/nm-tool.1*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/NetworkManager.conf

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnm-util.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnm-util.so.0
%attr(755,root,root) %{_libdir}/libnm_glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnm_glib.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnm-util.so
%attr(755,root,root) %{_libdir}/libnm_glib.so
%{_libdir}/libnm-util.la
%{_libdir}/libnm_glib.la
%{_includedir}/NetworkManager
%{_pkgconfigdir}/NetworkManager.pc
%{_pkgconfigdir}/libnm-util.pc
%{_pkgconfigdir}/libnm_glib.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnm-util.a
%{_libdir}/libnm_glib.a
