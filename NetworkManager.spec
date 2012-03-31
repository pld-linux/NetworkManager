#
# Conditional build
%bcond_with	systemd # rely on systemd for session tracking instead of ConsoleKit
%bcond_with	wimax	# enable wimax support
#
%define		ppp_version	2.4.5

Summary:	Network Manager for GNOME
Summary(pl.UTF-8):	Zarządca sieci dla GNOME
Name:		NetworkManager
Version:	0.9.4.0
Release:	1
Epoch:		2
License:	GPL v2+
Group:		Networking/Admin
Source0:	http://ftp.gnome.org/pub/GNOME/sources/NetworkManager/0.9/%{name}-%{version}.tar.xz
# Source0-md5:	66a54b51a4998c484613911b72a7e6ff
Source1:	%{name}.conf
Source2:	%{name}.upstart
Source3:	%{name}.tmpfiles
Patch0:		%{name}-pld.patch
Patch1:		ifcfg-path.patch
URL:		http://projects.gnome.org/NetworkManager/
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.10
BuildRequires:	dbus-devel >= 1.1.0
BuildRequires:	dbus-glib-devel >= 0.75
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel >= 0.17
BuildRequires:	glib2-devel >= 1:2.24.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	gtk-doc-automake >= 1.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libiw-devel >= 1:28-0.pre9.1
BuildRequires:	libnl-devel >= 3.0
BuildRequires:	libsoup-devel >= 2.26.0
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libuuid-devel
BuildRequires:	nss-devel >= 3.11
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.97
BuildRequires:	ppp-plugin-devel >= 3:%{ppp_version}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.629
BuildRequires:	sed >= 4.0
%{?with_systemd:BuildRequires:	systemd-devel}
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	udev-glib-devel >= 1:147
%{?with_wimax:BuildRequires:	wimax-devel >= 1.5.1}
BuildRequires:	xz
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	ConsoleKit-x11
Requires:	dhcp-client
Requires:	filesystem >= 3.0-37
Requires:	polkit >= 0.97
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 37-0.10
Requires:	wpa_supplicant >= 0.7.3-4
Suggests:	ModemManager
Suggests:	mobile-broadband-provider-info
Obsoletes:	NetworkManager-systemd
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
Requires:	dbus-glib >= 0.75
Requires:	glib2 >= 1:2.24.0
Requires:	nss >= 3.11
Requires:	udev-glib >= 1:147
Conflicts:	NetworkManager < 0.6.4-0.2

%description libs
Network Manager shared libraries.

%description libs -l pl.UTF-8
Biblioteki dzielone Network Managera.

%package devel
Summary:	Network Manager includes and more
Summary(pl.UTF-8):	Pliki nagłówkowe Network Managera
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	dbus-glib-devel >= 0.75
Requires:	glib2-devel >= 1:2.24.0
Requires:	libuuid-devel
Requires:	nss-devel >= 3.11
Requires:	udev-glib-devel >= 1:147

%description devel
Network Manager includes and more.

%description devel -l pl.UTF-8
Pliki nagłówkowe Network Manager.

%package static
Summary:	Network Manager static libraries
Summary(pl.UTF-8):	Statyczne biblioteki Network Managera
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Network Manager static libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Network Managera.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir} \
	--with-distro=pld \
	--enable-more-warnings=yes \
	--with-dhclient=/sbin/dhclient \
	--with-iptables=/usr/sbin/iptables \
	--with-system-ca-path=/etc/certs \
	--with-systemdsystemunitdir=%{systemdunitdir} \
	--with-session-tracking=%{?with_systemd:systemd}%{!?with_systemd:ck} \
	--with-pppd-plugin-dir=%{_libdir}/pppd/%{ppp_version} \
	--with-dist-version=%{version}-%{release} \
	--with-docs \
	%{__enable_disable wimax} \
	--enable-static

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/run/%{name},/usr/lib/tmpfiles.d} \
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/{VPN,dispatcher.d,system-connections}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

install -d $RPM_BUILD_ROOT/etc/init
cp -p %{SOURCE2} $RPM_BUILD_ROOT/etc/init/NetworkManager.conf

install %{SOURCE3} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf

# Cleanup
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/NetworkManager/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/pppd/%{ppp_version}/*.{a,la}

%find_lang %{name}

# examples
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version} -name 'Makefile*' | xargs rm

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add NetworkManager
%service -n NetworkManager restart "NetworkManager daemon"
%systemd_post NetworkManager.service NetworkManager-wait-online.service

%preun
if [ "$1" = "0" ]; then
	%service NetworkManager stop
	/sbin/chkconfig --del NetworkManager
fi
%systemd_preun NetworkManager.service NetworkManager-wait-online.service

%postun
%systemd_reload

%triggerpostun -- NetworkManager < 2:0.9.2.0-5
%systemd_trigger NetworkManager.service NetworkManager-wait-online.service

%triggerun -- NetworkManager < 0.7.0-0.svn4027.1
%service -q NetworkManagerDispatcher stop
/sbin/chkconfig --del NetworkManagerDispatcher

%triggerun -- NetworkManager < 0.8.9997-5
# move network interfaces description files to new location
mv -f /etc/sysconfig/network-scripts/ifcfg-* /etc/sysconfig/interfaces
mv -f /etc/sysconfig/network-scripts/keys-* /etc/sysconfig/interfaces
exit 0

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/nm-online
%attr(755,root,root) %{_bindir}/nm-tool
%attr(755,root,root) %{_bindir}/nmcli
%attr(755,root,root) %{_sbindir}/NetworkManager
%dir %{_libdir}/NetworkManager
%attr(755,root,root) %{_libdir}/NetworkManager/libnm-settings-plugin-ifcfg-rh.so
%attr(755,root,root) %{_libexecdir}/nm-avahi-autoipd.action
%attr(755,root,root) %{_libexecdir}/nm-dhcp-client.action
%attr(755,root,root) %{_libexecdir}/nm-dispatcher.action
%attr(755,root,root) %{_libexecdir}/nm-crash-logger
%attr(755,root,root) %{_libdir}/pppd/%{ppp_version}/nm-pppd-plugin.so
%attr(754,root,root) /etc/rc.d/init.d/NetworkManager
%config(noreplace) %verify(not md5 mtime size) /etc/init/NetworkManager.conf
%{systemdunitdir}/NetworkManager.service
%{systemdunitdir}/NetworkManager-wait-online.service
%{_datadir}/dbus-1/system-services/org.freedesktop.NetworkManager.service
/usr/lib/tmpfiles.d/%{name}.conf
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/gdb-cmd
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_datadir}/polkit-1/actions/org.freedesktop.NetworkManager.policy
/lib/udev/rules.d/77-nm-olpc-mesh.rules
%dir %{_sysconfdir}/%{name}/VPN
%dir %{_sysconfdir}/%{name}/system-connections
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/nm-dhcp-client.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/nm-avahi-autoipd.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/nm-dispatcher.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/nm-ifcfg-rh.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/org.freedesktop.NetworkManager.conf
%attr(700,root,root) %dir /var/run/%{name}
%attr(700,root,root) %dir /var/lib/%{name}
%{_mandir}/man1/nm-online.1*
%{_mandir}/man1/nm-tool.1*
%{_mandir}/man1/nmcli.1*
%{_mandir}/man5/nm-system-settings.conf.5*
%{_mandir}/man5/NetworkManager.conf.5*
%{_mandir}/man8/NetworkManager.8*
%{_examplesdir}/%{name}-%{version}

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/NetworkManager
%{_gtkdocdir}/libnm-glib
%{_gtkdocdir}/libnm-util

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnm-util.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnm-util.so.2
%attr(755,root,root) %{_libdir}/libnm-glib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnm-glib.so.4
%attr(755,root,root) %{_libdir}/libnm-glib-vpn.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnm-glib-vpn.so.1
%{_libdir}/girepository-1.0/NMClient-1.0.typelib
%{_libdir}/girepository-1.0/NetworkManager-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnm-util.so
%attr(755,root,root) %{_libdir}/libnm-glib.so
%attr(755,root,root) %{_libdir}/libnm-glib-vpn.so
%{_includedir}/NetworkManager
%{_includedir}/libnm-glib
%{_pkgconfigdir}/NetworkManager.pc
%{_pkgconfigdir}/libnm-util.pc
%{_pkgconfigdir}/libnm-glib-vpn.pc
%{_pkgconfigdir}/libnm-glib.pc
%{_datadir}/gir-1.0/NMClient-1.0.gir
%{_datadir}/gir-1.0/NetworkManager-1.0.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libnm-util.a
%{_libdir}/libnm-glib.a
%{_libdir}/libnm-glib-vpn.a
