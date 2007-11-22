# TODO:
# - add a working(!) pld backend... (it work's 4 me as it is now - czarny)
#
Summary:	Network Manager for GNOME
Summary(pl.UTF-8):	Zarządca sieci dla GNOME
Name:		NetworkManager
Version:	0.7
%define		_rev rev3104
Release:	0.%{_rev}.1
License:	GPL v2
Group:		X11/Applications
#Source0:	http://ftp.gnome.org/pub/GNOME/sources/NetworkManager/0.7/%{name}-%{version}.tar.bz2
Source0:	%{name}-%{version}%{_rev}.tar.bz2
# Source0-md5:	261b0672dfd21d5a99cbaae12e502006
Source1:	%{name}.init
Source2:	%{name}Dispatcher.init
Patch0:		%{name}-pld.patch
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.72
BuildRequires:	glib2-devel >= 1:2.10.0
BuildRequires:	gettext-devel
BuildRequires:	gnome-common
BuildRequires:	hal-devel >= 0.5.2
BuildRequires:	intltool >= 0.35.5
BuildRequires:	libiw-devel >= 1:28-0.pre9.1
BuildRequires:	ppp-plugin-devel
BuildRequires:	libnl-devel >= 1.0
BuildRequires:	libselinux-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dhcdbd
Requires:	rc-scripts
Requires:	wpa_supplicant >= 0.6-2
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

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
%setup -q -n %{name}-%{version}%{_rev}
%patch0 -p1

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--with-distro=pld
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/run/%{name},%{_sysconfdir}/%{name}/{VPN,dispatcher.d}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install test/nm-tool $RPM_BUILD_ROOT%{_bindir}/nm-tool

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/NetworkManager
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/NetworkManagerDispatcher


[ -d $RPM_BUILD_ROOT%{_datadir}/locale/sr@latin ] || \
	mv -f $RPM_BUILD_ROOT%{_datadir}/locale/sr@{Latn,latin}
%find_lang %{name} --with-gnome --all-name

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
%attr(755,root,root) %{_bindir}/nm-tool
%attr(755,root,root) %{_sbindir}/NetworkManager
%attr(755,root,root) %{_sbindir}/NetworkManagerDispatcher
%attr(755,root,root) %{_sbindir}/nm-system-settings
%dir %{_libdir}/NetworkManager
%attr(755,root,root) %{_libexecdir}/nm-crash-logger
%attr(755,root,root) %{_libdir}/nm-pppd-plugin.so
%attr(755,root,root) %{_libexecdir}/nm-dhcp-client.action
%attr(754,root,root) /etc/rc.d/init.d/NetworkManager
%attr(754,root,root) /etc/rc.d/init.d/NetworkManagerDispatcher
%dir %{_sysconfdir}/NetworkManager
%dir %{_sysconfdir}/NetworkManager/dispatcher.d
%dir %{_sysconfdir}/NetworkManager/VPN
%dir %{_datadir}/%{name}
%dir /var/run/%{name}
%{_datadir}/%{name}/gdb-cmd
%{_mandir}/man8/NetworkManager.8*
%{_mandir}/man8/NetworkManagerDispatcher.8*
%{_mandir}/man1/nm-tool.1*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/nm-dhcp-client.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/nm-system-settings.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/NetworkManager.conf

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnm-util.so.*.*.*
%attr(755,root,root) %{_libdir}/libnm_glib.so.*.*.*
%attr(755,root,root) %{_libdir}/libnm_glib_vpn.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnm-util.so
%attr(755,root,root) %{_libdir}/libnm_glib.so
%attr(755,root,root) %{_libdir}/libnm_glib_vpn.so
%{_libdir}/libnm-util.la
%{_libdir}/libnm_glib.la
%{_libdir}/libnm_glib_vpn.la
%{_includedir}/NetworkManager
%{_includedir}/libnm-glib
%{_pkgconfigdir}/NetworkManager.pc
%{_pkgconfigdir}/libnm-util.pc
%{_pkgconfigdir}/libnm_glib.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnm-util.a
%{_libdir}/libnm_glib.a
%{_libdir}/libnm_glib_vpn.a
