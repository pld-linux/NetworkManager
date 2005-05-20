Summary:	Network Manager for GNOME
Summary(pl):	Zarz±dca sieci dla GNOME
Name:		NetworkManager
Version:	0.4
Release:	0.20050520.1
License:	GPL v2
Group:		X11/Applications
#Source0:	http://ftp.gnome.org/pub/GNOME/sources/NetworkManager/0.3/%{name}-%{version}.tar.bz2
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	eea94f34fb8a5b2e662d78131c11f91d
Patch0:		%{name}-pld.patch
BuildRequires:	dbus-glib-devel >= 0.33
BuildRequires:	hal-devel >= 0.5.2
BuildRequires:	libiw-devel
Requires:		dhcdbd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Network Manager for GNOME.

%description -l pl
Zarz±dca sieci dla GNOME.

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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/nm-applet
%attr(755,root,root) %{_libdir}/lib*so.*
%{_datadir}/NetworkManager*
%{_sysconfdir}/dbus-1/system.d/*
%{_iconsdir}/*/*/apps/*.png
