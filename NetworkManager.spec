# TODO:
# - add a working(!) pld backend...
# - many files are not packaged (including init.d)
#
Summary:	Network Manager for GNOME
Summary(pl):	Zarz�dca sieci dla GNOME
Name:		NetworkManager
Version:	0.6.2
Release:	0.1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/NetworkManager/0.6/%{name}-%{version}.tar.bz2
# Source0-md5:	1254609e7d6a8de72677d63908bb4bd8
Source1:	%{name}.init
Patch0:		%{name}-pld.patch
BuildRequires:	dbus-glib-devel >= 0.6.3
BuildRequires:	dhcdbd
BuildRequires:	gnome-panel-devel
BuildRequires:	hal-devel >= 0.5.2
BuildRequires:	libiw-devel >= 28
BuildRequires:	libnl-devel >= 1.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	dhcdbd
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Network Manager for GNOME.

%description -l pl
Zarz�dca sieci dla GNOME.

%prep
%setup -q
%patch0 -p1

%build
autoreconf
%configure \
	--with-distro=pld
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/NetworkManager

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install
/sbin/chkconfig --add NetworkManager
%service NetworkManager restart "NetworkManager daemon"

%preun
if [ "$1" = "0" ]; then
	%service NetworkManager stop
	/sbin/chkconfig --del NetworkManager
fi

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_datadir}/nm-applet
%attr(755,root,root) %{_datadir}/gnome-vpn-properties
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/nm-crash-logger
%attr(754,root,root) /etc/rc.d/init.d/NetworkManager
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/gdb-cmd
%{_datadir}/gnome/autostart/*.desktop
%{_mandir}/man1/*
%{_sysconfdir}/dbus-1/system.d/*
%{_iconsdir}/*/*/apps/*.png

%if 0
# -devel?
%attr(755,root,root) %{_libdir}/libnm-util.so
%attr(755,root,root) %{_libdir}/libnm_glib.so
%{_libdir}/libnm-util.la
%{_libdir}/libnm_glib.la
%{_includedir}/NetworkManager
%{_pkgconfigdir}/NetworkManager.pc
%{_pkgconfigdir}/libnm-util.pc
%{_pkgconfigdir}/libnm_glib.pc

# -static?
%{_libdir}/libnm-util.a
%{_libdir}/libnm_glib.a
%endif
