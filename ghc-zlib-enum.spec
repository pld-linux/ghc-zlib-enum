#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	zlib-enum
Summary:	Enumerator interface for zlib compression
Summary(pl.UTF-8):	Interfejs enumeratora do kompresji zlib
Name:		ghc-%{pkgname}
Version:	0.2.3
Release:	2
License:	MIT
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/zlib-enum
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	dac776d2e3611187973301edbef9180a
URL:		http://hackage.haskell.org/package/zlib-enum
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.9
BuildRequires:	ghc-bytestring < 0.11
BuildRequires:	ghc-enumerator >= 0.4
BuildRequires:	ghc-enumerator < 0.5
BuildRequires:	ghc-transformers >= 0.2
BuildRequires:	ghc-transformers < 0.4
BuildRequires:	ghc-zlib-bindings >= 0.1
BuildRequires:	ghc-zlib-bindings < 0.2
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-bytestring-prof >= 0.9
BuildRequires:	ghc-bytestring-prof < 0.11
BuildRequires:	ghc-enumerator-prof >= 0.4
BuildRequires:	ghc-enumerator-prof < 0.5
BuildRequires:	ghc-transformers-prof >= 0.2
BuildRequires:	ghc-transformers-prof < 0.4
BuildRequires:	ghc-zlib-bindings-prof >= 0.1
BuildRequires:	ghc-zlib-bindings-prof < 0.2
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_releq	ghc
Requires:	ghc-base >= 4
Requires:	ghc-base < 5
Requires:	ghc-bytestring >= 0.9
Requires:	ghc-bytestring < 0.11
Requires:	ghc-enumerator >= 0.4
Requires:	ghc-enumerator < 0.5
Requires:	ghc-transformers >= 0.2
Requires:	ghc-transformers < 0.4
Requires:	ghc-zlib-bindings >= 0.1
Requires:	ghc-zlib-bindings < 0.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
zlib-enum is a stop-gap package to provide enumeratees for zlib
compression/decompression.

%description -l pl.UTF-8
zlib-enum to prowizoryczny pakiet zapewniający funkcje enumeratee
do kompresji/dekompresji zlib.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4
Requires:	ghc-base-prof < 5
Requires:	ghc-bytestring-prof >= 0.9
Requires:	ghc-bytestring-prof < 0.11
Requires:	ghc-enumerator-prof >= 0.4
Requires:	ghc-enumerator-prof < 0.5
Requires:	ghc-transformers-prof >= 0.2
Requires:	ghc-transformers-prof < 0.4
Requires:	ghc-zlib-bindings-prof >= 0.1
Requires:	ghc-zlib-bindings-prof < 0.2

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSzlib-enum-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSzlib-enum-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Zlib
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Zlib/*.hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSzlib-enum-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Zlib/*.p_hi
