# TODO: package /usr/lib/firewalld/zones/nm-shared.xml for firewalld support
#
# Conditional build
%bcond_without	systemd		# use systemd for session tracking instead of ConsoleKit (fallback to ConsoleKit on runtime)
%bcond_without	vala		# Vala API
%bcond_with	firewalld	# Firewalld zone for shared mode

Summary:	Network Manager for GNOME
Summary(pl.UTF-8):	Zarządca sieci dla GNOME
Name:		NetworkManager
Version:	1.32.0
Release:	1
Epoch:		2
License:	GPL v2+
Group:		Networking/Admin
Source0:	https://download.gnome.org/sources/NetworkManager/1.32/%{name}-%{version}.tar.xz
# Source0-md5:	637d790b4c4453cf04f141ed71e95957
Source1:	%{name}.conf
Source3:	%{name}.tmpfiles
Source4:	%{name}.init
Patch0:		ifcfg-path.patch
Patch1:		systemd-fallback.patch
URL:		https://wiki.gnome.org/Projects/NetworkManager
BuildRequires:	ModemManager-devel >= 1.0.0
BuildRequires:	audit-libs-devel
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.12
BuildRequires:	bluez-libs-devel >= 5.0
BuildRequires:	curl-devel >= 7.24.0
BuildRequires:	dbus-devel >= 1.1.0
BuildRequires:	gettext-tools >= 0.17
BuildRequires:	glib2-devel >= 1:2.38.0
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	gtk-doc-automake >= 1.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	jansson-devel >= 2.7
BuildRequires:	libndp-devel
BuildRequires:	libnl-devel >= 3.2.8
BuildRequires:	libpsl-devel >= 0.1
BuildRequires:	libselinux-devel
BuildRequires:	libteamdctl-devel >= 1.9
BuildRequires:	libtool >= 2:2.2
BuildRequires:	libuuid-devel
BuildRequires:	libxslt-progs
BuildRequires:	newt-devel >= 0.52.15
# also gnutls (>= 2.12) possible (--with-crypto=gnutls)
BuildRequires:	nss-devel >= 3.11
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.97
BuildRequires:	ppp-plugin-devel >= 3:2.4.6
BuildRequires:	python3 >= 1:3
BuildRequires:	python3-pygobject3
BuildRequires:	readline-devel
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	sed >= 4.0
%{?with_systemd:BuildRequires:	systemd-devel >= 1:209}
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel >= 1:175
%{?with_vala:BuildRequires:	vala >= 2:0.17.1.24}
BuildRequires:	xz
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
%if %{with systemd}
Suggests:	ConsoleKit-x11
%else
Requires:	ConsoleKit-x11
%endif
Requires:	curl-libs >= 7.24.0
Requires:	dhcp-client
Requires:	filesystem >= 3.0-37
Requires:	jansson >= 2.7
Requires:	libnl >= 3.2.8
Requires:	libpsl >= 0.1
Requires:	libteamdctl >= 1.9
Requires:	newt >= 0.52.15
Requires:	polkit >= 0.97
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 38
Requires:	wpa_supplicant >= 0.7.3-4
Suggests:	ModemManager >= 1.0.0
Suggests:	mobile-broadband-provider-info
Suggests:	resolvconf
Suggests:	teamd >= 1.9
Obsoletes:	NetworkManager-systemd
Obsoletes:	dhcdbd < 3.0-1
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		plugindir	%{_libdir}/NetworkManager
%define		distplugindir	%{plugindir}/%{version}-%{release}

%description
Network Manager for GNOME.

%description -l pl.UTF-8
Zarządca sieci dla GNOME.

%package apidocs
Summary:	libnm library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libnm
Group:		Documentation
Requires:	gtk-doc-common
BuildArch:	noarch

%description apidocs
libnm library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libnm.

%package libs
Summary:	Network Manager shared libraries
Summary(pl.UTF-8):	Biblioteki dzielone Network Managera
Group:		Libraries
Requires:	glib2 >= 1:2.38.0
Requires:	nss >= 3.11
Requires:	udev-libs >= 1:175
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
Requires:	glib2-devel >= 1:2.38.0
Requires:	libuuid-devel
Requires:	nss-devel >= 3.11

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

%package -n vala-NetworkManager
Summary:	Vala API for NetworkManager libraries
Summary(pl.UTF-8):	API języka Vala do bibliotek NetworkManagera
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Requires:	vala >= 2:0.17.1.24
BuildArch:	noarch

%description -n vala-NetworkManager
Vala API for NetworkManager libraries.

%description -n vala-NetworkManager -l pl.UTF-8
API języka Vala do bibliotek NetworkManagera.

%package -n bash-completion-NetworkManager
Summary:	Bash completion for NetworkManager command (nmcli)
Summary(pl.UTF-8):	Bashowe uzupełnianie nazw dla polecenia NetworkManagera (nmcli)
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-NetworkManager
Bash completion for NetworkManager command (nmcli).

%description -n bash-completion-NetworkManager -l pl.UTF-8
Bashowe uzupełnianie nazw dla polecenia NetworkManagera (nmcli).

%prep
%setup -q
%patch0 -p1
%{?with_systemd:%patch1 -p1}

grep -rl /usr/bin/env examples | xargs sed -i -e '1{
	s,^#!.*bin/env gjs,#!/usr/bin/gjs,
	s,^#!.*bin/env lua,#!%{__lua},
	s,^#!.*bin/env python,#!%{__python},
	s,^#!.*bin/env ruby,#!%{__ruby},
}'


%build
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--enable-ifcfg-rh \
	--enable-more-warnings \
	--disable-silent-rules \
	--enable-static \
	%{!?with_vala:--disable-vala} \
	--with-dhclient=/sbin/dhclient \
	--with-dhcpcd=/sbin/dhcpcd \
	%{!?with_firewalld:--disable-firewalld-zone} \
	--with-html-dir=%{_gtkdocdir} \
	--with-iptables=/usr/sbin/iptables \
	--with-iwd=yes \
	--with-nft=/usr/sbin/nft \
	--with-nmcli \
	--with-system-ca-path=/etc/certs \
	--with-systemdsystemunitdir=%{systemdunitdir} \
	--with-session-tracking=%{?with_systemd:systemd}%{!?with_systemd:ck} \
	--with-suspend-resume=%{?with_systemd:systemd}%{!?with_systemd:upower} \
	--with-pppd=/usr/sbin/pppd \
	--with-pppd-plugin-dir=%{_libdir}/pppd/plugins \
	--with-resolvconf=/sbin/resolvconf \
	--with-udev-dir=/lib/udev \
	--with-dist-version=%{version}-%{release}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,/var/run/%{name},%{systemdtmpfilesdir}} \
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/{VPN,conf.d,dispatcher.d,dnsmasq.d,dnsmasq-shared.d,system-connections} \
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/dispatcher.d/{pre-down.d,pre-up.d,no-wait.d} \
	$RPM_BUILD_ROOT%{_prefix}/lib/%{name}/{VPN,conf.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE4} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

cp -p %{SOURCE3} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

# Cleanup
%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{distplugindir}/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/pppd/plugins/*.{a,la}

%find_lang %{name}

# examples
%{__make} clean-checkPROGRAMS

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

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

%triggerun -- NetworkManager < 0.8.9997-5
# < 0.7.0-0.svn4027.1: disable obsolete service
if /sbin/chkconfig --list | grep -q NetworkManagerDispatcher ; then
	%service -q NetworkManagerDispatcher stop
	/sbin/chkconfig --del NetworkManagerDispatcher
fi
# < 0.8.9997-5: move network interfaces description files to new location
mv -f /etc/sysconfig/network-scripts/ifcfg-* /etc/sysconfig/interfaces
mv -f /etc/sysconfig/network-scripts/keys-* /etc/sysconfig/interfaces
exit 0

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/nm-online
%attr(755,root,root) %{_bindir}/nmcli
%attr(755,root,root) %{_bindir}/nmtui
%attr(755,root,root) %{_bindir}/nmtui-connect
%attr(755,root,root) %{_bindir}/nmtui-edit
%attr(755,root,root) %{_bindir}/nmtui-hostname
%attr(755,root,root) %{_sbindir}/NetworkManager
%dir %{plugindir}
%dir %{distplugindir}
%attr(755,root,root) %{distplugindir}/libnm-device-plugin-adsl.so
%attr(755,root,root) %{distplugindir}/libnm-device-plugin-bluetooth.so
%attr(755,root,root) %{distplugindir}/libnm-device-plugin-ovs.so
%attr(755,root,root) %{distplugindir}/libnm-device-plugin-wifi.so
%attr(755,root,root) %{distplugindir}/libnm-device-plugin-wwan.so
%attr(755,root,root) %{distplugindir}/libnm-device-plugin-team.so
%attr(755,root,root) %{distplugindir}/libnm-ppp-plugin.so
%attr(755,root,root) %{distplugindir}/libnm-settings-plugin-ifcfg-rh.so
%attr(755,root,root) %{distplugindir}/libnm-wwan.so
%attr(755,root,root) %{_libexecdir}/nm-cloud-setup
%attr(755,root,root) %{_libexecdir}/nm-daemon-helper
%attr(755,root,root) %{_libexecdir}/nm-dhcp-helper
%attr(755,root,root) %{_libexecdir}/nm-dispatcher
%attr(755,root,root) %{_libexecdir}/nm-iface-helper
%attr(755,root,root) %{_libexecdir}/nm-ifdown
%attr(755,root,root) %{_libexecdir}/nm-ifup
%attr(755,root,root) %{_libexecdir}/nm-initrd-generator
%attr(755,root,root) %{_libdir}/pppd/plugins/nm-pppd-plugin.so
%attr(754,root,root) /etc/rc.d/init.d/NetworkManager
%if "%{_lib}" != "lib"
%dir %{_prefix}/lib/NetworkManager
%endif
%dir %{_prefix}/lib/NetworkManager/VPN
%dir %{_prefix}/lib/NetworkManager/conf.d
%dir %{_prefix}/lib/NetworkManager/dispatcher.d
%{_prefix}/lib/NetworkManager/dispatcher.d/90-nm-cloud-setup.sh
%dir %{_prefix}/lib/NetworkManager/dispatcher.d/no-wait.d
%attr(755,root,root) %{_prefix}/lib/NetworkManager/dispatcher.d/no-wait.d/90-nm-cloud-setup.sh
%{systemdunitdir}/NetworkManager.service
%{systemdunitdir}/NetworkManager-dispatcher.service
%{systemdunitdir}/NetworkManager-wait-online.service
%{systemdunitdir}/nm-cloud-setup.service
%{systemdunitdir}/nm-cloud-setup.timer
%dir %{systemdunitdir}/NetworkManager.service.d
%{systemdunitdir}/NetworkManager.service.d/NetworkManager-ovs.conf
%{systemdtmpfilesdir}/%{name}.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_datadir}/dbus-1/system.d/nm-dispatcher.conf
%{_datadir}/dbus-1/system.d/nm-ifcfg-rh.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.NetworkManager.conf
%{_datadir}/polkit-1/actions/org.freedesktop.NetworkManager.policy
/lib/udev/rules.d/84-nm-drivers.rules
/lib/udev/rules.d/85-nm-unmanaged.rules
/lib/udev/rules.d/90-nm-thunderbolt.rules
%dir %{_sysconfdir}/%{name}/VPN
%dir %{_sysconfdir}/%{name}/conf.d
%dir %{_sysconfdir}/%{name}/dispatcher.d
%dir %{_sysconfdir}/%{name}/dispatcher.d/pre-down.d
%dir %{_sysconfdir}/%{name}/dispatcher.d/pre-up.d
%dir %{_sysconfdir}/%{name}/dispatcher.d/no-wait.d
%dir %{_sysconfdir}/%{name}/dnsmasq.d
%dir %{_sysconfdir}/%{name}/dnsmasq-shared.d
%dir %{_sysconfdir}/%{name}/system-connections
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%attr(711,root,root) %dir /var/run/%{name}
%attr(700,root,root) %dir /var/lib/%{name}
%{_mandir}/man1/nm-online.1*
%{_mandir}/man1/nmcli.1*
%{_mandir}/man1/nmtui-connect.1*
%{_mandir}/man1/nmtui-edit.1*
%{_mandir}/man1/nmtui-hostname.1*
%{_mandir}/man1/nmtui.1*
%{_mandir}/man5/NetworkManager.conf.5*
%{_mandir}/man5/nm-settings.5*
%{_mandir}/man5/nm-settings-dbus.5*
%{_mandir}/man5/nm-settings-ifcfg-rh.5*
%{_mandir}/man5/nm-settings-keyfile.5*
%{_mandir}/man5/nm-settings-nmcli.5*
%{_mandir}/man5/nm-system-settings.conf.5*
%{_mandir}/man7/nm-openvswitch.7*
%{_mandir}/man7/nmcli-examples.7*
%{_mandir}/man8/NetworkManager.8*
%{_mandir}/man8/NetworkManager-dispatcher.8*
%{_mandir}/man8/nm-cloud-setup.8*
%{_mandir}/man8/nm-initrd-generator.8*
%{_examplesdir}/%{name}-%{version}

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/NetworkManager
%{_gtkdocdir}/libnm

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnm.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnm.so.0
%{_libdir}/girepository-1.0/NM-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnm.so
%{_includedir}/libnm
%{_pkgconfigdir}/libnm.pc
%{_datadir}/dbus-1/interfaces/org.freedesktop.NetworkManager.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.NetworkManager.*.xml
%{_datadir}/gir-1.0/NM-1.0.gir

%files static
%defattr(644,root,root,755)
%{_libdir}/libnm.a

%if %{with vala}
%files -n vala-NetworkManager
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/libnm.deps
%{_datadir}/vala/vapi/libnm.vapi
%endif

%files -n bash-completion-NetworkManager
%defattr(644,root,root,755)
%{bash_compdir}/nmcli
