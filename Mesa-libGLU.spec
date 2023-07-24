#
# Conditional build:
%bcond_without	glvnd		# use GLVND as OpenGL provider
%bcond_with	osmesa		# use OSMesa as OpenGL provider
%bcond_without	static_libs	# static library
#
%if %{without glvnd} && %{without osmesa}
%define	with_generic_opengl	1
%endif
Summary:	SGI implementation of libGLU OpenGL library
Summary(pl.UTF-8):	Implementacja SGI biblioteki libGLU ze standardu OpenGL
Name:		Mesa-libGLU
Version:	9.0.3
Release:	1
License:	SGI Free Software License B v2.0 (MIT-like)
Group:		Libraries
Source0:	https://archive.mesa3d.org/glu/glu-%{version}.tar.xz
# Source0-md5:	06a4fff9179a98ea32ef41b6d83f6b19
URL:		https://www.mesa3d.org/
%{?with_osmesa:BuildRequires:	Mesa-libOSMesa-devel}
%{?with_generic_opengl:BuildRequires:	OpenGL-devel >= 1.2}
%{?with_glvnd:BuildRequires:	libglvnd-libGL-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	meson >= 0.52.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
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
%{?with_osmesa:Requires:	Mesa-libOSMesa-devel}
%{?with_generic_opengl:Requires:	OpenGL-devel >= 1.2}
%{?with_glvnd:Requires:	libglvnd-libGL-devel}
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
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	%{!?with_glvnd:-Dgl_provider=%{?with_osmesa:osmesa}%{!?with_osmesa:gl}}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

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
%{_pkgconfigdir}/glu.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libGLU.a
%endif
