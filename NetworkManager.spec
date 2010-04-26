Summary:	Network Manager for GNOME
Summary(pl.UTF-8):	Zarządca sieci dla GNOME
Name:		NetworkManager
Version:	0.8
Release:	2
License:	GPL v2
Group:		Networking/Admin
Source0:	http://ftp.gnome.org/pub/GNOME/sources/NetworkManager/0.8/%{name}-%{version}.tar.bz2
# Source0-md5:	d343e22f132754696654511acde354c2
Source1:	%{name}-system-settings.conf
Patch0:		%{name}-pld.patch
URL:		http://projects.gnome.org/NetworkManager/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel >= 1.1.0
BuildRequires:	dbus-glib-devel >= 0.75
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.18.0
BuildRequires:	gtk-doc-automake
BuildRequires:	intltool >= 0.35.5
BuildRequires:	libiw-devel >= 1:28-0.pre9.1
BuildRequires:	libnl-devel >= 1:1.0-0.pre8.1
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	nss-devel >= 3.11
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel
BuildRequires:	ppp-plugin-devel >= 3:2.4.4-2
BuildRequires:	rpmbuild(macros) >= 1.450
BuildRequires:	sed >= 4.0
BuildRequires:	udev-devel
BuildRequires:	udev-glib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dhcp-client
Requires:	polkit
Requires:	rc-scripts
Requires:	wpa_supplicant >= 0.6-2
Obsoletes:	dhcdbd < 3.0-1
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
Network Manager for GNOME.

%description -l pl.UTF-8
Zarządca sieci dla GNOME.

%package apidocs
Summary:	libnm-glib library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libnm-glib
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libnm-glib library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libnm-glib.

%package libs
Summary:	Network Manager shared libraries
Summary(pl.UTF-8):	Biblioteki dzielone Network Managera
Group:		Libraries
Conflicts:	NetworkManager < 0.6.4-0.2

%description libs
Network Manager shared libraries.

%description libs -l pl.UTF-8
Biblioteki dzielone Network Managera.

%package devel
Summary:	Network Manager includes and more
Summary(pl.UTF-8):	Pliki nagłówkowe Network Managera
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-glib-devel >= 0.75
Requires:	libuuid-devel

%description devel
Network Manager includes and more.

%description devel -l pl.UTF-8
Pliki nagłówkowe Network Manager.

%package static
Summary:	Network Manager static libraries
Summary(pl.UTF-8):	Statyczne biblioteki Network Managera
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Network Manager static libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Network Managera.

%prep
%setup -q
%patch0 -p1

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-html-dir=%{_gtkdocdir} \
	--with-distro=pld \
	--with-dhcp-client=/sbin/dhclient \
	--with-iptables=/usr/sbin/iptables \
	--with-system-ca-path=/etc/certs

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/run/%{name},%{_sysconfdir}/%{name}/{VPN,dispatcher.d}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/NetworkManager/nm-system-settings.conf

# Cleanup
rm -f $RPM_BUILD_ROOT%{_libexecdir}/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/pppd/2.4.4/*.{a,la}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add NetworkManager
%service -n NetworkManager restart "NetworkManager daemon"

%preun
if [ "$1" = "0" ]; then
	%service NetworkManager stop
	/sbin/chkconfig --del NetworkManager
fi

%triggerun -- NetworkManager < 0.7.0-0.svn4027.1
%service -q NetworkManagerDispatcher stop
/sbin/chkconfig --del NetworkManagerDispatcher

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/nm-tool
%attr(755,root,root) %{_sbindir}/NetworkManager
%dir %{_libdir}/NetworkManager
%attr(755,root,root) %{_libexecdir}/nm-crash-logger
%attr(755,root,root) %{_libdir}/pppd/2.4.4/nm-pppd-plugin.so
%attr(755,root,root) %{_libexecdir}/nm-avahi-autoipd.action
%attr(755,root,root) %{_libexecdir}/nm-dhcp-client.action
%attr(755,root,root) %{_libexecdir}/nm-dispatcher.action
%attr(755,root,root) %{_libexecdir}/libnm-settings-plugin-keyfile.so
%attr(754,root,root) /etc/rc.d/init.d/NetworkManager
/lib/udev/rules.d/77-nm-olpc-mesh.rules
%dir %{_sysconfdir}/NetworkManager
%dir %{_sysconfdir}/NetworkManager/VPN
%dir %{_sysconfdir}/NetworkManager/dispatcher.d
%dir %{_sysconfdir}/NetworkManager/system-connections
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/NetworkManager/nm-system-settings.conf
%dir %{_datadir}/%{name}
%dir /var/run/%{name}
%{_datadir}/polkit-1/actions/org.freedesktop.network-manager-settings.system.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_datadir}/%{name}/gdb-cmd
%{_mandir}/man8/NetworkManager.8*
%{_mandir}/man1/nm-tool.1*
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/nm-dhcp-client.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/nm-avahi-autoipd.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/nm-dispatcher.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/NetworkManager.conf

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libnm-glib
%{_gtkdocdir}/libnm-util

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnm-util.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnm-util.so.1
%attr(755,root,root) %{_libdir}/libnm-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnm-glib.so.2
%attr(755,root,root) %{_libdir}/libnm-glib-vpn.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnm-glib-vpn.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnm-util.so
%attr(755,root,root) %{_libdir}/libnm-glib.so
%attr(755,root,root) %{_libdir}/libnm-glib-vpn.so
%{_libdir}/libnm-util.la
%{_libdir}/libnm-glib.la
%{_libdir}/libnm-glib-vpn.la
%{_includedir}/NetworkManager
%{_includedir}/libnm-glib
%{_pkgconfigdir}/NetworkManager.pc
%{_pkgconfigdir}/libnm-util.pc
%{_pkgconfigdir}/libnm-glib-vpn.pc
%{_pkgconfigdir}/libnm-glib.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnm-util.a
%{_libdir}/libnm-glib.a
%{_libdir}/libnm-glib-vpn.a
