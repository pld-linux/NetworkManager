%define		ppp_version	2.4.5
Summary:	Network Manager for GNOME
Summary(pl.UTF-8):	Zarządca sieci dla GNOME
Name:		NetworkManager
Version:	0.8.2
Release:	4
Epoch:		1
License:	GPL v2+
Group:		Networking/Admin
Source0:	http://ftp.gnome.org/pub/GNOME/sources/NetworkManager/0.8/%{name}-%{version}.tar.bz2
# Source0-md5:	951158258544f761d9c09c052a7072e2
Source1:	%{name}.conf
Patch0:		%{name}-pld.patch
Patch1:		%{name}-compile.patch
Patch2:		upstart.patch
URL:		http://projects.gnome.org/NetworkManager/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-devel >= 1.1.0
BuildRequires:	dbus-glib-devel >= 0.75
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 1:2.18.0
BuildRequires:	gtk-doc
BuildRequires:	gtk-doc-automake >= 1.0
BuildRequires:	intltool >= 0.35.5
BuildRequires:	libiw-devel >= 1:28-0.pre9.1
BuildRequires:	libnl1-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	nss-devel >= 3.11
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel
BuildRequires:	ppp-plugin-devel >= 3:%{ppp_version}
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.450
BuildRequires:	sed >= 4.0
BuildRequires:	udev-devel
BuildRequires:	udev-glib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
Requires:	dhcp-client
Requires:	filesystem >= 3.0-37
Requires:	polkit
Requires:	rc-scripts >= 0.4.3.0
Requires:	wpa_supplicant >= 0.6-2
Suggests:	ModemManager
Suggests:	mobile-broadband-provider-info
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
Requires:	glib2 >= 1:2.18.0
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
Requires:	glib2-devel >= 1:2.18.0
Requires:	libuuid-devel
Requires:	udev-glib-devel

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
%if "%{pld_release}" == "th"
%patch2 -p1
%endif

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
	--enable-more-warnings=yes \
	--with-dhclient=/sbin/dhclient \
	--with-iptables=/usr/sbin/iptables \
	--with-system-ca-path=/etc/certs \
	--with-pppd-plugin-dir=%{_libdir}/pppd/%{ppp_version} \
	--with-dist-version=%{version}-%{release} \
	--with-docs

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/run/%{name},%{_sysconfdir}/%{name}/{VPN,dispatcher.d,system-connections}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

# Cleanup
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
%attr(755,root,root) %{_bindir}/nmcli
%attr(755,root,root) %{_sbindir}/NetworkManager
%dir %{_libdir}/NetworkManager
%attr(755,root,root) %{_libdir}/NetworkManager/libnm-settings-plugin-keyfile.so
%attr(755,root,root) %{_libdir}/NetworkManager/libnm-settings-plugin-ifcfg-rh.so
%attr(755,root,root) %{_libexecdir}/nm-avahi-autoipd.action
%attr(755,root,root) %{_libexecdir}/nm-dhcp-client.action
%attr(755,root,root) %{_libexecdir}/nm-dispatcher.action
%attr(755,root,root) %{_libexecdir}/nm-crash-logger
%attr(755,root,root) %{_libdir}/pppd/%{ppp_version}/nm-pppd-plugin.so
%attr(754,root,root) /etc/rc.d/init.d/NetworkManager
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/gdb-cmd
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_datadir}/polkit-1/actions/org.freedesktop.NetworkManager.policy
%{_datadir}/polkit-1/actions/org.freedesktop.network-manager-settings.system.policy
/lib/udev/rules.d/77-nm-olpc-mesh.rules
%dir %{_sysconfdir}/%{name}/VPN
%dir %{_sysconfdir}/%{name}/system-connections
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/nm-dhcp-client.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/nm-avahi-autoipd.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/nm-dispatcher.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/nm-ifcfg-rh.conf
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/NetworkManager.conf
%dir /var/run/%{name}
%{_mandir}/man1/nm-online.1*
%{_mandir}/man1/nm-tool.1*
%{_mandir}/man1/nmcli.1*
%{_mandir}/man5/nm-system-settings.conf.5*
%{_mandir}/man5/NetworkManager.conf.5*
%{_mandir}/man8/NetworkManager.8*
%{_examplesdir}/%{name}-%{version}

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
