#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	SGI implementation of libGLU OpenGL library
Summary(pl.UTF-8):	Implementacja SGI biblioteki libGLU ze standardu OpenGL
Name:		Mesa-libGLU
Version:	9.0.0
Release:	1
License:	SGI Free Software License B v2.0 (MIT-like)
Group:		Libraries
Source0:	ftp://ftp.freedesktop.org/pub/mesa/glu/glu-%{version}.tar.bz2
# Source0-md5:	be9249132ff49275461cf92039083030
URL:		http://www.mesa3d.org/
BuildRequires:	OpenGL-devel >= 1.2
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2.2
BuildRequires:	pkgconfig
Requires:	OpenGL >= 1.2
Provides:	OpenGL-GLU = 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SGI implementation of libGLU OpenGL library. It implements OpenGL GLU
1.3 specifications.

%description -l pl.UTF-8
Implementacja SGI biblioteki libGLU ze standardu OpenGL. Implementuje
specyfikację OpenGL GLU 1.3.

%package devel
Summary:	Header files for SGI libGLU library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SGI libGLU
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	OpenGL-devel >= 1.2
Provides:	OpenGL-GLU-devel = 1.3

%description devel
Header files for SGI libGLU library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SGI libGLU.

%package static
Summary:	Static SGI libGLU library
Summary(pl.UTF-8):	Statyczna biblioteka SGI libGLU
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	OpenGL-GLU-static = 1.3

%description static
Static SGI libGLU library.

%description static -l pl.UTF-8
Statyczna biblioteka SGI libGLU.

%prep
%setup -q -n glu-%{version}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# there is pkg-config support; also, traditionally libGLU didn't have .la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libGLU.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLU.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libGLU.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libGLU.so
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h
%{_pkgconfigdir}/glu.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libGLU.a
%endif
